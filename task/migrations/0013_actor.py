# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-08-23 08:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0012_auto_20180823_1502'),
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actorId', models.CharField(max_length=5)),
                ('act_status', models.IntegerField(default=0)),
                ('task_describe', models.TextField(max_length=200)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task.Task')),
            ],
        ),
    ]
