import base64
from datetime import datetime as dt
import time
import re

import boto.s3.connection
import pytz

import catflap.settings as settings
from catflapsite.obj.custom import FakeKey, ImgUrl
from catflapsite.utils import constants


# CONNECTION MODEL #
class S3Conn(object):
    def __init__(self):
        self.client = boto.s3.connect_to_region("eu-west-2", aws_access_key_id=settings.AWS_KEY, is_secure=False,
                                                aws_secret_access_key=settings.AWS_SECRET,
                                                calling_format=boto.s3.connection.OrdinaryCallingFormat())
        self.bucket = self.client.get_bucket(settings.IMAGE_BUCKET)

    def raw_keys(self, start=None, n=18, previous_key=None):
        rf = 4 if n < 100 else 5
        keys = []
        listlen = n if start is None else start + n
        if previous_key is not None:
            prefix = re.search(constants.REGEXES["file_timestamp"], previous_key).groups()[0].split("_")[0][:-rf]
        else:
            prefix = str(time.time()).split(".")[0][:-rf]
        while len(keys) < listlen:
            keys_with_prefix = self.bucket.get_all_keys(prefix=constants.FILE_PREFIX + prefix)
            key_section = sorted([k for k in keys_with_prefix if k.name.split(".")[-1] in constants.ACCEPTED_FILES.keys()],
                key=lambda x: x.last_modified, reverse=True)
            maxlen = min(listlen, len(key_section))
            if previous_key is not None:
                try:
                    ix = key_section.index(previous_key) + 1
                except ValueError:
                    ix = 0
                keys += key_section[ix:ix + maxlen]
            keys += key_section[:maxlen]
            rounded = float(prefix + ("0" * rf))
            prefix = str(rounded - int("1" + ("0" * rf))).split(".")[0][:-rf]
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
        return self.bucket.get_key(filename, validate=False)

    def get_cat_from_url(self, url):
        filename = url.split("/")[-1].split("?")[0]
        cat = self.bucket.get_key(filename, validate=False)
        if not cat.exists():
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


# UTILITY METHODS #
def localise(t):
    london = pytz.timezone("Europe/London")
    return london.localize(t)


def now():
    return localise(dt.now())


def decode_filename(b64imgid):
    bytesid = bytes(b64imgid, "utf-8")
    b64id = base64.urlsafe_b64decode(bytesid)
    decodeid = b64id.decode()
    filename = decodeid.replace(settings.SALT, "").split("?")[0]
    return filename


def get_cats_from_objects(url_objects, page_start, page_end, fields, first_only=False):
    imgs = {}
    urls = url_objects.distinct("url").order_by("url")
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
