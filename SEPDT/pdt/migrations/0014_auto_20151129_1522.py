# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdt', '0013_auto_20151129_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='developer',
            name='projects',
            field=models.ManyToManyField(blank=True, related_name='developers', to='pdt.Project'),
        ),
        migrations.AlterField(
            model_name='manager',
            name='projects',
            field=models.ManyToManyField(blank=True, related_name='managers', to='pdt.Project'),
        ),
    ]
