import base64
import math
import re
from datetime import datetime as dt

import requests

from catflap import settings as settings
from catflapsite.utils.constants import ACCEPTED_FILES, AWS_HEADERS, SCHRODINGER, INSIDE, OUTSIDE
from catflapsite.utils.db import localise, now


class FakeKey(object):
    def __init__(self, url):
        self.name = url.split("/")[-1].split("?")[0]
        response = requests.get(url)
        if response.ok:
            self.size = len(response.content)
        else:
            self.size = 0
        self.ok = response.ok
        self.__url = url

    def generate_url(self, **kwargs):
        return self.__url


class ImgUrl(object):
    def __init__(self, key):
        self.filename = key.name
        self.filetype = ACCEPTED_FILES[key.name.split(".")[-1]]
        try:
            self.time_taken = localise(dt.fromtimestamp(float(re.search(".+_(\d+_\d+)[^\d]+", key.name).groups()[0].replace("_", "."))))
        except:
            self.time_taken = localise(dt.now())
        self.id = base64.urlsafe_b64encode((self.filename + settings.SALT).encode())
        self.size = key.size
        self.url = key.generate_url(expires_in=0, query_auth=False, response_headers= AWS_HEADERS)
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