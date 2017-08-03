import base64
from datetime import datetime as dt

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

    @property
    def raw_keys(self):
        return list(reversed(
            sorted([k for k in self.bucket.get_all_keys() if k.name.split(".")[-1] in constants.ACCEPTED_FILES.keys()],
                   key=lambda x: x.last_modified)))

    @property
    def custom_keys(self):
        return [ImgUrl(k) for k in self.raw_keys]

    @property
    def cats(self):
        return [k for k in self.custom_keys if k.iscat]

    @property
    def notcats(self):
        return [k for k in self.custom_keys if not k.iscat]

    @property
    def latest_cat(self):
        return next(k for k in self.custom_keys if k.iscat)

    def get_key(self, b64imgid):
        filename = decode_filename(b64imgid)
        return self.bucket.get_key(filename, validate = False)

    def get_cat_from_url(self, url):
        filename = url.split("/")[-1].split("?")[0]
        cat = self.bucket.get_key(filename, validate = False)
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


def get_cats_from_objects(url_objects, page_start, page_end, fields, first_only = False):
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
