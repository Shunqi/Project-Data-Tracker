# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdt', '0010_auto_20151125_1814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='developer',
            name='projects',
            field=models.ManyToManyField(to='pdt.Project', blank=True),
        ),
        migrations.AlterField(
            model_name='manager',
            name='projects',
            field=models.ManyToManyField(to='pdt.Project', blank=True),
        ),
    ]
