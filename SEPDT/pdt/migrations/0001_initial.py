# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityTime',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'Development', max_length=20)),
                ('time_used', models.DurationField()),
            ],
        ),
        migrations.CreateModel(
            name='DefectData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data_type', models.CharField(max_length=1, choices=[(b'R', b'Requirements'), (b'D', b'Design'), (b'I', b'Implementation'), (b'B', b'Bad fix')])),
            ],
        ),
        migrations.CreateModel(
            name='Developer',
            fields=[
                ('employee_id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Iteration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('iteration_id', models.IntegerField(default=1)),
                ('code_size', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('employee_id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Phase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phase_id', models.IntegerField(default=1, choices=[(1, b'Inception'), (2, b'Elaboration'), (3, b'Construction'), (4, b'Transition')])),
                ('num_of_iteration', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('project_id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=20)),
                ('description', models.CharField(max_length=60)),
            ],
        ),
        migrations.AddField(
            model_name='phase',
            name='project',
            field=models.ForeignKey(to='pdt.Project'),
        ),
        migrations.AddField(
            model_name='manager',
            name='projects',
            field=models.ManyToManyField(to='pdt.Project'),
        ),
        migrations.AddField(
            model_name='iteration',
            name='phase',
            field=models.ForeignKey(to='pdt.Phase'),
        ),
        migrations.AddField(
            model_name='developer',
            name='projects',
            field=models.ManyToManyField(to='pdt.Project'),
        ),
        migrations.AddField(
            model_name='defectdata',
            name='developer',
            field=models.ForeignKey(to='pdt.Developer'),
        ),
        migrations.AddField(
            model_name='defectdata',
            name='inject_iteration',
            field=models.ForeignKey(related_name='defectdata_inject_iteration', to='pdt.Iteration'),
        ),
        migrations.AddField(
            model_name='defectdata',
            name='remove_iteration',
            field=models.ForeignKey(related_name='defectdata_remove_iteration', to='pdt.Iteration'),
        ),
        migrations.AddField(
            model_name='activitytime',
            name='developer',
            field=models.ForeignKey(to='pdt.Developer'),
        ),
        migrations.AddField(
            model_name='activitytime',
            name='iteration',
            field=models.ForeignKey(to='pdt.Iteration'),
        ),
    ]
