# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-08-19 12:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_auto_20180817_1624'),
    ]

    operations = [
        migrations.CreateModel(
            name='Edition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('projectName', models.CharField(max_length=30)),
                ('editionNum', models.CharField(max_length=50)),
                ('environment', models.CharField(max_length=20)),
                ('createTime', models.DateTimeField(auto_now=True)),
                ('status', models.IntegerField()),
                ('downloadLink', models.CharField(max_length=100)),
                ('describe', models.TextField(max_length=200)),
            ],
        ),
    ]
