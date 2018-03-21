# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdt', '0003_auto_20151119_1832'),
    ]

    operations = [
        migrations.CreateModel(
            name='Metrics',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'myName', max_length=20)),
                ('SLOC', models.DecimalField(default=0, max_digits=10, decimal_places=3)),
                ('effot', models.DecimalField(default=0, max_digits=10, decimal_places=3)),
                ('code_effot', models.DecimalField(default=0, max_digits=10, decimal_places=3)),
                ('inject_num', models.IntegerField(default=0)),
                ('remove_num', models.IntegerField(default=0)),
                ('inject_rate', models.DecimalField(default=0, max_digits=10, decimal_places=3)),
                ('remove_rate', models.DecimalField(default=0, max_digits=10, decimal_places=3)),
                ('defect_density', models.DecimalField(default=0, max_digits=10, decimal_places=3)),
                ('m_yield', models.DecimalField(default=0, max_digits=10, decimal_places=3)),
            ],
        ),
        migrations.AddField(
            model_name='iteration',
            name='metrics',
            field=models.ForeignKey(default=1, to='pdt.Metrics'),
        ),
        migrations.AddField(
            model_name='phase',
            name='metrics',
            field=models.ForeignKey(default=1, to='pdt.Metrics'),
        ),
        migrations.AddField(
            model_name='project',
            name='metrics',
            field=models.ForeignKey(default=1, to='pdt.Metrics'),
        ),
    ]
