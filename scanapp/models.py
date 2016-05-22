from __future__ import unicode_literals

from django.db import models


class Scanmodel(models.Model):
    email = models.TextField(max_length=200)
    resultsurl = models.TextField(max_length=2000)
    status = models.TextField(max_length=11)
    location = models.TextField(max_length=500)
