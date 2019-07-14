import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = os.environ['DJANGO_DEBUG']

IMAGE_BUCKET = os.environ['IMAGE_BUCKET']

AWS_KEY = os.environ['AWS_KEY']

AWS_SECRET = os.environ['AWS_SECRET']

SALT = os.environ['SALT']