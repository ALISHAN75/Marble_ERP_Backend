# Generated by Django 4.1 on 2022-11-17 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0003_alter_earning_transaction_items_earn_trans_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense_transaction_items',
            name='ITEM_RATE_UNIT',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
        ),
        migrations.AlterField(
            model_name='expense_transaction_items',
            name='ITEM_UNIT_QUANTITY',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
        ),
        migrations.AlterField(
            model_name='expense_transactions',
            name='TOTAL_wTAX',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
