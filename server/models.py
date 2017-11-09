from __future__ import unicode_literals
from django.db import models


# Create your models here. 数据模块 使用ORM框架
class GuitarSheet(models.Model):
    link = models.TextField(null=False)
    title = models.TextField(null=False)

    # def __str__(self):
    #     return self


