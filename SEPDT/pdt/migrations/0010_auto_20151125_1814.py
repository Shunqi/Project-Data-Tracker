# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pdt', '0009_auto_20151124_1922'),
    ]

    operations = [
        migrations.AddField(
            model_name='developer',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='manager',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL, default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='activitytime',
            name='name',
            field=models.CharField(max_length=20, default='Development'),
        ),
        migrations.AlterField(
            model_name='defectdata',
            name='data_type',
            field=models.CharField(max_length=1, choices=[('R', 'Requirement'), ('D', 'Design'), ('I', 'Implementation'), ('B', 'Bad fix')]),
        ),
        migrations.AlterField(
            model_name='defectdata',
            name='description',
            field=models.CharField(max_length=200, default=''),
        ),
        migrations.AlterField(
            model_name='metrics',
            name='name',
            field=models.CharField(max_length=20, default='myName'),
        ),
        migrations.AlterField(
            model_name='phase',
            name='phase_id',
            field=models.IntegerField(default=1, choices=[(1, 'Inception'), (2, 'Elaboration'), (3, 'Construction'), (4, 'Transition')]),
        ),
    ]
