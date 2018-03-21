# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdt', '0012_auto_20151129_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iteration',
            name='metrics',
            field=models.ForeignKey(to='pdt.Metrics', default=1, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='phase',
            name='metrics',
            field=models.ForeignKey(to='pdt.Metrics', default=1, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='current_ite',
            field=models.ForeignKey(to='pdt.Iteration', default=1, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='metrics',
            field=models.ForeignKey(to='pdt.Metrics', default=1, null=True, blank=True),
        ),
    ]
