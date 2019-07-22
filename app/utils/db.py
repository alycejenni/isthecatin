import re
from datetime import datetime as dt

import boto3
from botocore.exceptions import ClientError

from app.obj.custom import FakeKey, ImgUrl
from app.utils import constants
from app.utils.utils import decode_filename
from config.settings import env as settings


# CONNECTION MODEL
class S3Conn(object):
    def __init__(self):
        self.client = boto3.client('s3',
                                   aws_access_key_id=settings.AWS_KEY,
                                   aws_secret_access_key=settings.AWS_SECRET,
                                   region_name='eu-west-2')
        self.s3 = boto3.resource('s3',
                                 aws_access_key_id=settings.AWS_KEY,
                                 aws_secret_access_key=settings.AWS_SECRET,
                                 region_name='eu-west-2'
                                 )
        self.bucket = self.s3.Bucket(settings.IMAGE_BUCKET)

    def raw_keys(self, start=None, n=18, previous_key=None):
        rf = 5 if n < 100 else 6
        keys = []
        listlen = n if start is None else start + n
        if previous_key is not None:
            prefix = \
            re.search(constants.REGEXES['file_timestamp'], previous_key).groups()[0].split('_')[0][
            :-rf]
        else:
            # start with now and work backwards
            prefix_timestamp = dt.timestamp(dt.now())
        while len(keys) < listlen:
            prefix = str(prefix_timestamp)[:6]
            keys_with_prefix = self.bucket.objects.filter(Prefix=constants.FILE_PREFIX + prefix)
            key_section = sorted(
                [k for k in keys_with_prefix],
                key=lambda x: x.last_modified, reverse=True)
            maxlen = min(listlen, len(key_section))
            if previous_key is not None:
                try:
                    ix = key_section.index(previous_key) + 1
                except ValueError:
                    ix = 0
                keys += key_section[ix:ix + maxlen]
            keys += key_section[:maxlen]
            prefix_timestamp -= 10000
        return keys[0 if start is None else start:listlen]

    def custom_keys(self, start=0, n=18):
        return [ImgUrl(k) for k in self.raw_keys(start, n)]

    def cats(self, start=0, n=18):
        return [k for k in self.custom_keys(start, n) if k.iscat]

    def notcats(self, start=0, n=18):
        return [k for k in self.custom_keys(start, n) if not k.iscat]

    @property
    def latest_cat(self):
        return next(k for k in self.custom_keys(0, 1) if k.iscat)

    def get_key(self, b64imgid):
        filename = decode_filename(b64imgid)
        return self.bucket.Object(filename)

    def get_cat_from_url(self, url):
        filename = url.split('/')[-1].split('?')[0]
        cat = self.bucket.Object(filename)
        try:
            cat.load()
        except ClientError:
            cat = FakeKey(url)
            if not cat.ok:
                return None
        return ImgUrl(cat)

    def set_not_cat(self, b64imgid):
        filename = decode_filename(b64imgid)
        new_key = "not a cat/" + filename
        self.bucket.copy_key(new_key, settings.IMAGE_BUCKET, filename)
        self.bucket.delete_key(filename)

    def delete_key(self, b64imgid):
        filename = decode_filename(b64imgid)
        self.bucket.delete_key(filename)

    def set_cat(self, b64imgid):
        filename = decode_filename(b64imgid)
        new_key = filename.replace("not%20a%20cat", "")
        self.bucket.copy_key(new_key, settings.IMAGE_BUCKET, filename)
        self.bucket.delete_key(filename)


# UTILITY METHODS
def get_cats_from_objects(url_objects, page_start, page_end, fields, first_only=False):
    imgs = {}
    urls = url_objects.distinct("url").order_by("url")
    print(urls)
    if page_end is not None:
        urls = urls[page_start:page_end]
    for i in urls:
        if page_end is not None and len(imgs) == page_end - page_start:
            break
        obj = url_objects.filter(url__exact=i.url)
        img = conn.get_cat_from_url(i.url)
        if img is None:
            continue
        imgs[img.id] = {
            "media": img
            }
        fields.append("pk")
        for field in fields:
            if first_only:
                imgs[img.id][field] = getattr(obj[0], field)
            else:
                imgs[img.id][field] = [getattr(o, field) for o in obj]
    return [imgs[i] for i in imgs]


conn = S3Conn()
