# Generated by Django 4.1 on 2022-11-17 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0006_alter_expense_transaction_items_rec_add_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='earning_transaction_items',
            name='REC_ADD_BY',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]