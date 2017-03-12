import pytz
from datetime import datetime as dt
import boto
import catflap.settings as settings
import base64

AWS_HEADERS = {
    "Cache-Control": "public, max-age=86400"
    }


class ImgUrl(object):
    def __init__(self, key):
        self.filename = key.name
        self.time_taken = localise(dt.strptime(key.last_modified, "%Y-%m-%dT%H:%M:%S.000Z"))
        self.id = base64.urlsafe_b64encode((self.filename + settings.SALT).encode())
        self.size = key.size
        self.url = key.generate_url(expires_in=0, query_auth=False, response_headers=AWS_HEADERS)

    @property
    def time_ago(self):
        return now() - self.time_taken

    @property
    def iscat(self):
        try:
            return "not%20a%20cat" not in self.url
        except:
            return True  # always assume cat


class S3Conn(object):
    def __init__(self):
        self.client = boto.connect_s3(settings.AWS_KEY, settings.AWS_SECRET, host="s3.eu-west-2.amazonaws.com")
        self.bucket = self.client.get_bucket(settings.IMAGE_BUCKET)

    @property
    def raw_keys(self):
        return list(reversed(
            sorted([k for k in self.bucket.get_all_keys() if k.name.endswith(".jpg")], key=lambda x: x.last_modified)))

    @property
    def custom_keys(self):
        return [ImgUrl(k) for k in self.raw_keys]

    @property
    def cats(self):
        return [k for k in self.custom_keys if k.iscat]

    @property
    def latest_cat(self):
        return next(k for k in self.custom_keys if k.iscat)

    def get_key(self, b64imgid):
        filename = decode_filename(b64imgid)
        return self.bucket.get_key(filename, validate=False)

    def set_not_cat(self, b64imgid):
        filename = decode_filename(b64imgid)
        new_key = "not a cat/" + filename
        self.bucket.copy_key(new_key, settings.IMAGE_BUCKET, filename)
        self.bucket.delete_key(filename)


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


conn = S3Conn()
