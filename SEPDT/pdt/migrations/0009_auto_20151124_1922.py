# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdt', '0008_auto_20151120_1511'),
    ]

    operations = [
        migrations.AddField(
            model_name='defectdata',
            name='description',
            field=models.CharField(default=b'', max_length=200),
        ),
        migrations.AlterField(
            model_name='defectdata',
            name='data_type',
            field=models.CharField(max_length=1, choices=[(b'R', b'Requirement'), (b'D', b'Design'), (b'I', b'Implementation'), (b'B', b'Bad fix')]),
        ),
        migrations.AlterField(
            model_name='iteration',
            name='code_size',
            field=models.IntegerField(default=0),
        ),
    ]
