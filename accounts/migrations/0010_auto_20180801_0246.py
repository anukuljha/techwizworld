# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-01 02:46
from __future__ import unicode_literals

import datetime
import django.core.validators
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20180711_1346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billedproducts',
            name='quantity',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='bills',
            name='invoice_date',
            field=models.DateField(default=datetime.datetime(2018, 8, 1, 2, 46, 8, 234235, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='bills',
            name='po_date',
            field=models.DateField(default=datetime.datetime(2018, 8, 1, 2, 46, 8, 234260, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='quantity',
            field=models.FloatField(default=1, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='productrate',
            name='unit',
            field=models.CharField(choices=[(b'KG', b'KG'), (b'Pcs', b'Pcs'), (b'Pkt', b'Pkt'), (b'Ltr', b'Ltr'), (b'Tin', b'Tin'), (b'Bottle', b'Bottle'), (b'Metre', b'Metre'), (b'Box', b'Box')], default=b'KG', max_length=10),
        ),
        migrations.AlterField(
            model_name='purchasebill',
            name='purchase_date',
            field=models.DateField(default=datetime.datetime(2018, 8, 1, 2, 46, 8, 233156, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='purchasedproduct',
            name='unit',
            field=models.CharField(choices=[(b'KG', b'KG'), (b'Pcs', b'Pcs'), (b'Pkt', b'Pkt'), (b'Ltr', b'Ltr'), (b'Tin', b'Tin'), (b'Bottle', b'Bottle'), (b'Metre', b'Metre'), (b'Box', b'Box')], default=b'KG', max_length=10),
        ),
    ]
