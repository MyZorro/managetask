# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-08-22 01:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0008_task_task_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='task',
            new_name='edition',
        ),
    ]
