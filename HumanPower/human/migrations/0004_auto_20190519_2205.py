# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-19 13:05
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('human', '0003_human_coordinates'),
    ]

    operations = [
        migrations.AddField(
            model_name='human',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='case',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(null=True, srid=4326, verbose_name='工作地點'),
        ),
    ]
