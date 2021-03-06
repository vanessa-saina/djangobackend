# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-04-08 16:50
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20180408_1650'),
    ]

    operations = [
        migrations.AddField(
            model_name='myunit',
            name='unit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='unit', to='users.Unit'),
        ),
        migrations.AddField(
            model_name='myunit',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]
