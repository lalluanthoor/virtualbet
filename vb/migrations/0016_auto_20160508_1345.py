# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-08 13:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vb', '0015_auto_20160507_0349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configuration',
            name='max_receiver_amount',
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='configuration',
            name='max_transfer_amount',
            field=models.IntegerField(default=-1),
        ),
    ]