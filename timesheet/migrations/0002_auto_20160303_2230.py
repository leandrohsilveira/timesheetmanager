# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-04 01:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('timesheet', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoDocumento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=200)),
                ('abreviacao', models.CharField(max_length=10)),
            ],
        ),
        migrations.AlterField(
            model_name='documento',
            name='tipo_documento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timesheet.TipoDocumento'),
        ),
    ]
