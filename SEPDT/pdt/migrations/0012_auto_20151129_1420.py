# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdt', '0011_auto_20151126_1958'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='developer',
            name='employee_id',
        ),
        migrations.RemoveField(
            model_name='developer',
            name='name',
        ),
        migrations.RemoveField(
            model_name='manager',
            name='employee_id',
        ),
        migrations.RemoveField(
            model_name='manager',
            name='name',
        ),
        migrations.AddField(
            model_name='developer',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, default=1, auto_created=True, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='manager',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, default=1, auto_created=True, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
