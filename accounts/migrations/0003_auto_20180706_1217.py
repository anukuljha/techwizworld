# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-07-06 06:47
from __future__ import unicode_literals

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20180706_0238'),
    ]

    operations = [
        migrations.CreateModel(
            name='PurchaseBill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchase_date', models.DateField(default=datetime.datetime(2018, 7, 6, 6, 47, 24, 43268, tzinfo=utc))),
                ('seller', models.CharField(max_length=100)),
                ('collection', models.CharField(choices=[('1', '(CGST/SGST)'), ('2', '(IGST)')], default=1, max_length=100)),
                ('seller_GSTIN', models.CharField(max_length=30)),
                ('seller_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Site')),
            ],
        ),
        migrations.CreateModel(
            name='PurchasedProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('quantity', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
            ],
        ),
        migrations.CreateModel(
            name='SaleSummary',
            fields=[
            ],
            options={
                'verbose_name': 'Sale Summary',
                'verbose_name_plural': 'Sales Summary',
                'proxy': True,
                'indexes': [],
            },
            bases=('accounts.billedproducts',),
        ),
        migrations.RemoveField(
            model_name='bills',
            name='to',
        ),
        migrations.RemoveField(
            model_name='product',
            name='inventory',
        ),
        migrations.AlterField(
            model_name='billedproducts',
            name='category',
            field=models.IntegerField(choices=[(0, 0), (5, 5), (12, 12), (18, 18)]),
        ),
        migrations.AlterField(
            model_name='bills',
            name='invoice_date',
            field=models.DateField(default=datetime.datetime(2018, 7, 6, 6, 47, 24, 43268, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='purchasedproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Product'),
        ),
        migrations.AddField(
            model_name='purchasedproduct',
            name='purchase_bill',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.PurchaseBill'),
        ),
    ]
