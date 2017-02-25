import pytz
from datetime import datetime as dt
import boto
import catflap.settings as settings

def localise(t):
    london = pytz.timezone("Europe/London")
    return london.localize(t)

def now():
    return localise(dt.now())

def get_all_s3():
    s3 = boto.connect_s3(settings.AWS_KEY, settings.AWS_SECRET, host = "s3.eu-west-2.amazonaws.com")
    bucket = s3.get_bucket(settings.IMAGE_BUCKET)
    return list(reversed(sorted(bucket.get_all_keys(), key = lambda x: x.last_modified)))

def get_latest_s3():
    return get_all_s3()[0]

class ImgUrl(object):
    def __init__(self, s3_obj):
        self.url = s3_obj.generate_url(expires_in=0, query_auth=False)
        self.time_taken = localise(dt.strptime(s3_obj.last_modified, "%Y-%m-%dT%H:%M:%S.000Z"))

    @property
    def time_ago(self):
        return now() - self.time_taken
