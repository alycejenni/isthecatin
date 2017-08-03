from django.db import models


class Casualty(models.Model):
    url = models.URLField()
    time_taken = models.DateTimeField()
    creature_type = models.CharField(max_length = 100)
    creature_name = models.CharField(max_length = 100)
    doa = models.BooleanField()
    known_deceased = models.BooleanField()
    additional_image = models.URLField()
    guilty_cat = models.URLField()


class Highlight(models.Model):
    url = models.URLField()
    comment = models.CharField(max_length = 255)