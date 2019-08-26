# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-07-11 08:16
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20180710_1949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bills',
            name='invoice_date',
            field=models.DateField(default=datetime.datetime(2018, 7, 11, 8, 16, 18, 144256, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='bills',
            name='invoice_number',
            field=models.IntegerField(default=0, unique=True),
        ),
        migrations.AlterField(
            model_name='bills',
            name='po_date',
            field=models.DateField(default=datetime.datetime(2018, 7, 11, 8, 16, 18, 144256, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='purchasebill',
            name='purchase_date',
            field=models.DateField(default=datetime.datetime(2018, 7, 11, 8, 16, 18, 143253, tzinfo=utc)),
        ),
    ]
