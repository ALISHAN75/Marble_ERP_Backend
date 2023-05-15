# Generated by Django 4.1 on 2022-11-03 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logistics', '0005_deliveries_totl_dlvry_ordr_cost_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deliveries',
            old_name='TOTL_DLVRY_ORDR_COST',
            new_name='DLVRY_ORDR_COST',
        ),
        migrations.AddField(
            model_name='deliveries',
            name='DLVRY_wORDR_COST',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]