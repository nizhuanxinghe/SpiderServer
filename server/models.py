from __future__ import unicode_literals
from django.db import models


# Create your models here. 数据模块 使用ORM框架
class GuitarSheet(models.Model):
    link = models.TextField(null=False)
    title = models.TextField(null=False)


class ConfigParam(models.Model):
    macAddress = models.TextField(null=False)
    rootUrl = models.TextField(null=False)
    urlTag = models.TextField(null=False)
    pageTitle = models.TextField(null=False)
    pageClass = models.TextField(null=False)
    objClass = models.TextField(null=False)
    objTagClass = models.TextField(null=False)
    filter = models.TextField(null=False)

