# Generated by Django 4.1 on 2022-11-18 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0011_alter_earning_transaction_items_item_desc_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='earning_transactions',
            name='REC_ADD_BY',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='expense_transactions',
            name='REC_ADD_BY',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
