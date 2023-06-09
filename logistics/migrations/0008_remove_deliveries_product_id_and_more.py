# Generated by Django 4.1 on 2022-11-04 06:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_alter_orders_delvry_sts_alter_orders_ordr_no'),
        ('logistics', '0007_deliveries_product_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deliveries',
            name='PRODUCT_ID',
        ),
        migrations.AddField(
            model_name='delivery_items',
            name='PRODUCT_ID',
            field=models.ForeignKey(db_column='PRODUCT_ID', default=1, on_delete=django.db.models.deletion.CASCADE, related_name='lg_product_id', to='inventory.products'),
        ),
    ]
