import pytz
from datetime import datetime as dt
import boto.s3.connection
import catflap.settings as settings
import base64
import re
import math
import requests

AWS_HEADERS = {
    "Cache-Control": "public, max-age=86400"
}

INSIDE = 1
OUTSIDE = 0
SCHRODINGER = 2

ACCEPTED_FILES = {
    "jpg": "img",
    "mp4": "video"
}


class FakeKey(object):
    def __init__(self, url):
        self.name = url.split("/")[-1].split("?")[0]
        response = requests.get(url)
        if response.ok:
            self.size = len(response.content)
        else:
            self.size = 200
        self.__url = url

    def generate_url(self, **kwargs):
        return self.__url


class ImgUrl(object):
    def __init__(self, key):
        self.filename = key.name
        self.filetype = ACCEPTED_FILES[key.name.split(".")[-1]]
        try:
            self.time_taken = localise(dt.fromtimestamp(float(re.search(".+_(\d+_\d+)[^\d]+", key.name).groups()[0].replace("_", "."))))
        except AttributeError:
            self.time_taken = localise(dt.now())
        self.id = base64.urlsafe_b64encode((self.filename + settings.SALT).encode())
        self.size = key.size
        self.url = key.generate_url(expires_in=0, query_auth=False, response_headers=AWS_HEADERS)
        self.httpurl = key.generate_url(expires_in=0, query_auth=False, force_http=True)
        if "-" not in key.name:
            self.direction = SCHRODINGER
        else:
            if key.name.split("-")[-1].split(".")[0] == "1":
                self.direction = INSIDE
            else:
                self.direction = OUTSIDE

    @property
    def time_ago(self):
        return now() - self.time_taken

    @property
    def time_ago_str(self):
        timeago = self.time_ago
        days = timeago.days
        hours = math.floor(timeago.seconds / 3600)
        if hours > 1:
            hp = "s"
        else:
            hp = ""
        minutes = math.floor((timeago.seconds - (hours * 3600)) / 60)
        if minutes > 1:
            mp = "s"
        else:
            mp = ""

        if days < 1 and hours > 0:
            return f"{hours} hour{hp} and {minutes} minute{mp}"
        elif days < 1 and hours == 0 and minutes > 0:
            return f"{minutes} minute{mp}"
        elif days < 1 and hours == 0 and minutes == 0:
            return "less than a minute"
        else:
            return f"{days} days, {hours} hour{hp}, and {minutes} minute{mp}"

    @property
    def iscat(self):
        try:
            return "not%20a%20cat" not in self.url
        except:
            return True  # always assume cat


class S3Conn(object):
    def __init__(self):
        self.client = boto.s3.connect_to_region("eu-west-2", aws_access_key_id=settings.AWS_KEY, is_secure=False,
                                                aws_secret_access_key=settings.AWS_SECRET,
                                                calling_format=boto.s3.connection.OrdinaryCallingFormat())
        self.bucket = self.client.get_bucket(settings.IMAGE_BUCKET)

    @property
    def raw_keys(self):
        return list(reversed(
            sorted([k for k in self.bucket.get_all_keys() if k.name.split(".")[-1] in ACCEPTED_FILES.keys()],
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
        return cat

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
        img = ImgUrl(conn.get_cat_from_url(i.url))
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