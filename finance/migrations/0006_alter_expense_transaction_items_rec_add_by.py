# Generated by Django 4.1 on 2022-11-17 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0005_alter_expense_transaction_items_item_rate_unit_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense_transaction_items',
            name='REC_ADD_BY',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
