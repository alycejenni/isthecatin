from django.db import models


class Image(models.Model):
    imgdata = models.BinaryField()
    timetaken = models.DateTimeField()