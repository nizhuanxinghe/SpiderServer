# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-08 03:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GuitarSheet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.TextField(null=True)),
                ('title', models.TextField(default='title', null=True)),
            ],
        ),
    ]
