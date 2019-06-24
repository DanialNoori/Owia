# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-06-24 14:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_address', models.CharField(max_length=200)),
                ('activated', models.BooleanField(default=False)),
            ],
        ),
    ]
