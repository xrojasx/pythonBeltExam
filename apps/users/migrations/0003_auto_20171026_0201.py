# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-10-26 02:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20171026_0139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='dob',
            field=models.DateField(blank=True, max_length=8, null=True),
        ),
    ]
