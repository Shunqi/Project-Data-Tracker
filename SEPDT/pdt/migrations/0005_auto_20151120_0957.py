# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdt', '0004_auto_20151120_0945'),
    ]

    operations = [
        migrations.RenameField(
            model_name='metrics',
            old_name='code_effot',
            new_name='code_effort',
        ),
        migrations.RenameField(
            model_name='metrics',
            old_name='effot',
            new_name='effort',
        ),
    ]
