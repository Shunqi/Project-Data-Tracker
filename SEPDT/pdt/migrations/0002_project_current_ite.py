# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdt', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='current_ite',
            field=models.ForeignKey(default=1, to='pdt.Iteration'),
        ),
    ]
