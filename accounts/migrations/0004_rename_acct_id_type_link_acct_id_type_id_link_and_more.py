# Generated by Django 4.1 on 2022-12-01 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_account_type_accounts_acct_desc_ur_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='acct_id_type_link',
            new_name='acct_id_type_id_link',
        ),
        migrations.AddField(
            model_name='acct_ledger',
            name='TRANSC_DESC_UR',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='cashledger',
            name='TRANSC_DESC_UR',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='FIRST_NAME',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='LAST_NAME',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterModelTable(
            name='acct_id_type_id_link',
            table='acct_id_type_id_link',
        ),
        migrations.AlterModelTable(
            name='acct_ledger',
            table='acct_ledger',
        ),
        migrations.AlterModelTable(
            name='cashledger',
            table='cash_ledger',
        ),
    ]