# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-14 10:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bracketVisualizer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='bracketBatch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batchNumber', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='bracketMatch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('winnerURL', models.CharField(max_length=200)),
                ('winnerName', models.CharField(max_length=200)),
                ('winnerProsent', models.DecimalField(decimal_places=1, max_digits=3)),
                ('loserURL', models.CharField(max_length=200)),
                ('loserName', models.CharField(max_length=200)),
                ('loserProsent', models.DecimalField(decimal_places=1, max_digits=3)),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bracketVisualizer.bracketBatch')),
            ],
        ),
        migrations.DeleteModel(
            name='bracketModel',
        ),
    ]