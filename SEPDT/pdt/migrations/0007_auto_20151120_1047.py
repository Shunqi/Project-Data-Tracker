# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdt', '0006_auto_20151120_1015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activitytime',
            name='time_used',
            field=models.IntegerField(default=0),
        ),
    ]
