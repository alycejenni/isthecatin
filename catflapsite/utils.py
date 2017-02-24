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
    return sorted(bucket.get_all_keys(), key = lambda x: x.last_modified)

def get_latest_s3():
    return get_all_s3()[-1]