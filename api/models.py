from django.db import models


class Language(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField(max_length=256, blank=True)

