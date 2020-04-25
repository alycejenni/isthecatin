import base64
from datetime import datetime as dt

import pytz

from config.settings import env as settings


def localise(t):
    london = pytz.timezone('Europe/London')
    return london.localize(t)


def now():
    return localise(dt.now())


def decode_filename(b64imgid):
    bytesid = bytes(b64imgid, 'utf-8')
    b64id = base64.urlsafe_b64decode(bytesid)
    decodeid = b64id.decode()
    filename = decodeid.replace(settings.SALT, '').split('?')[0]
    return filename
