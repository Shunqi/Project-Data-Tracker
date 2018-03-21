# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdt', '0007_auto_20151120_1047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metrics',
            name='SLOC',
            field=models.DecimalField(default=-1, max_digits=10, decimal_places=3),
        ),
    ]
