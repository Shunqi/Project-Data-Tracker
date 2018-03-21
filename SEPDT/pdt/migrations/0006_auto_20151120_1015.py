# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdt', '0005_auto_20151120_0957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metrics',
            name='effort',
            field=models.DecimalField(default=-1, max_digits=10, decimal_places=3),
        ),
    ]
