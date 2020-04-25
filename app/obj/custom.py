import base64
import math
import re
from datetime import datetime as dt

import requests

import app.utils.utils
from config.settings import env as settings
from app.utils import constants
from app.utils import db


class FakeKey(object):
    def __init__(self, url):
        self.name = url.split('/')[-1].split('?')[0]
        response = requests.get(url)
        self.ok = response.ok
        self.__url = url

    def generate_url(self, **kwargs):
        return self.__url


class ImgUrl(object):
    def __init__(self, key):
        self.filename = key.key
        self.filetype = constants.ACCEPTED_FILES[key.key.split('.')[-1]]
        try:
            self.time_taken = app.utils.utils.localise(dt.fromtimestamp(
                float(re.search(constants.REGEXES['file_timestamp'], key.key).groups()[0].replace('_', '.'))))
        except:
            self.time_taken = app.utils.utils.localise(dt.now())
        self.id = base64.urlsafe_b64encode((self.filename + settings.SALT).encode())
        self.url = db.conn.client.generate_presigned_url('get_object', Params={'Bucket': settings.IMAGE_BUCKET, 'Key': key.key}).split('?')[0]
        self.httpurl = db.conn.client.generate_presigned_url('get_object', Params={'Bucket': settings.IMAGE_BUCKET, 'Key': key.key}, HttpMethod='http').split('?')[0]
        if '-' not in key.key:
            self.direction = constants.SCHRODINGER
        else:
            if key.key.split('-')[-1].split('.')[0] == '1':
                self.direction = constants.INSIDE
            else:
                self.direction = constants.OUTSIDE

    @property
    def time_ago(self):
        return app.utils.utils.now() - self.time_taken

    @property
    def time_ago_str(self):
        timeago = self.time_ago
        days = timeago.days
        hours = math.floor(timeago.seconds / 3600)
        if hours > 1:
            hp = 's'
        else:
            hp = ''
        minutes = math.floor((timeago.seconds - (hours * 3600)) / 60)
        if minutes > 1:
            mp = 's'
        else:
            mp = ''

        if days < 1 and hours > 0:
            return f'{hours} hour{hp} and {minutes} minute{mp}'
        elif days < 1 and hours == 0 and minutes > 0:
            return f'{minutes} minute{mp}'
        elif days < 1 and hours == 0 and minutes == 0:
            return 'less than a minute'
        else:
            return f'{days} days, {hours} hour{hp}, and {minutes} minute{mp}'

    @property
    def iscat(self):
        try:
            return 'not%20a%20cat' not in self.url
        except:
            return True  # always assume cat
