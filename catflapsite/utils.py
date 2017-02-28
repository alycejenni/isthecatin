import pytz
from datetime import datetime as dt
import boto
import catflap.settings as settings
import base64
from boto.s3.key import Key
import os.path


def localise(t):
    london = pytz.timezone("Europe/London")
    return london.localize(t)

def now():
    return localise(dt.now())

def get_bucket():
    s3 = boto.connect_s3(settings.AWS_KEY, settings.AWS_SECRET, host = "s3.eu-west-2.amazonaws.com")
    return s3.get_bucket(settings.IMAGE_BUCKET)

def get_all_s3():
    bucket = get_bucket()
    return list(reversed(sorted([k for k in bucket.get_all_keys() if k.name.endswith(".jpg")], key = lambda x: x.last_modified)))

def get_latest_s3():
    return next(k for k in get_all_s3() if "not%20a%20cat" not in k.generate_url(expires_in=0, query_auth=False))

class ImgUrl(object):
    def __init__(self, s3_obj):
        self.url = s3_obj.generate_url(expires_in=0, query_auth=False)
        self.time_taken = localise(dt.strptime(s3_obj.last_modified, "%Y-%m-%dT%H:%M:%S.000Z"))
        self.filename = self.url.split("/")[-1]
        self.id = base64.urlsafe_b64encode((self.filename + settings.SALT).encode())

    @property
    def time_ago(self):
        return now() - self.time_taken

    @property
    def iscat(self):
        try:
            return load_tags()[self.id]
        except:
            return True  # always assume cat


def get_key(b64img):
    filename = base64.b64decode(b64img).decode().replace(settings.SALT, "")
    return Key(get_bucket(), filename)


def load_tags():
    if os.path.isfile(settings.NOT_CAT):
        try:
            with open(settings.NOT_CAT, "r") as file:
                return [l.strip() for l in file.readlines()]
        except EOFError:
            return []


def set_not_cat(imgid):
    tags = load_tags()
    if tags is None:
        tags = []
    tags.append(base64.b64decode(bytes(imgid, "utf-8")).decode().replace(settings.SALT, ""))
    with open(settings.NOT_CAT, "w") as file:
        file.write("\n".join(tags))
