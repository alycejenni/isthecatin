import pytz
from datetime import datetime as dt
import boto
import catflap.settings as settings
import base64
from boto.s3.key import Key
import os.path

AWS_HEADERS = { "Cache-Control": "public, max-age=86400" }


class ImgUrl(object):
    def __init__(self, s3_obj):
        self.url = s3_obj.generate_url(expires_in = 0, query_auth = False, response_headers = AWS_HEADERS)
        self.time_taken = localise(dt.strptime(s3_obj.last_modified, "%Y-%m-%dT%H:%M:%S.000Z"))
        self.filename = self.url.split("/")[-1]
        self.id = base64.urlsafe_b64encode((self.filename + settings.SALT).encode())

    @property
    def time_ago(self):
        return now() - self.time_taken

    @property
    def iscat(self):
        try:
            return "not%20a%20cat" not in self.url
        except:
            return True  # always assume cat


def localise(t):
    london = pytz.timezone("Europe/London")
    return london.localize(t)


def now():
    return localise(dt.now())


def get_bucket():
    s3 = boto.connect_s3(settings.AWS_KEY, settings.AWS_SECRET, host = "s3.eu-west-2.amazonaws.com")
    return s3.get_bucket(settings.IMAGE_BUCKET)


def get_raw_keys():
    bucket = get_bucket()
    return list(reversed(
        sorted([k for k in bucket.get_all_keys() if k.name.endswith(".jpg")], key = lambda x: x.last_modified)))


def get_key_objects():
    return [ImgUrl(k) for k in get_raw_keys()]


def get_latest_s3():
    return next(k for k in get_key_objects() if k.iscat)


def get_key(b64img):
    filename = base64.b64decode(b64img).decode().replace(settings.SALT, "")
    return Key(get_bucket(), filename)


def set_not_cat(imgid):
    filename = base64.b64decode(bytes(imgid, "utf-8")).decode().replace(settings.SALT, "").split("?")[0]
    bucket = get_bucket()
    bucket.copy_key("not a cat/" + filename, settings.IMAGE_BUCKET, filename)
    bucket.delete_key(filename)