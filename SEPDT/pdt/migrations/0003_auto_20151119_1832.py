# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdt', '0002_project_current_ite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activitytime',
            name='time_used',
            field=models.IntegerField(),
        ),
    ]
