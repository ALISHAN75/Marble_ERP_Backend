# Generated by Django 4.1 on 2022-10-22 06:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CashLedger',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('ORDINAL', models.IntegerField(blank=True, null=True)),
                ('TRANSC_DESC', models.CharField(blank=True, max_length=255, null=True)),
                ('EARNING', models.FloatField(null=True)),
                ('EXPENSE', models.FloatField(null=True)),
                ('BALANCE', models.FloatField(null=True)),
                ('REC_ADD_DT', models.DateTimeField(auto_now_add=True)),
                ('REC_ADD_BY', models.IntegerField(default=1)),
                ('ACCT_ID', models.ForeignKey(db_column='ACCT_ID', null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.accounts')),
            ],
            options={
                'db_table': 'CASH_LEDGER',
            },
        ),
        migrations.CreateModel(
            name='Acct_Ledger',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('ORDINAL', models.IntegerField(blank=True, null=True)),
                ('TRANSC_DESC', models.CharField(blank=True, max_length=255, null=True)),
                ('EARNING', models.FloatField(null=True)),
                ('EXPENSE', models.FloatField(null=True)),
                ('BALANCE', models.FloatField(null=True)),
                ('REC_ADD_DT', models.DateTimeField(auto_now_add=True)),
                ('REC_ADD_BY', models.IntegerField(default=1)),
                ('ACCT_ID', models.ForeignKey(db_column='ACCT_ID', on_delete=django.db.models.deletion.CASCADE, to='accounts.accounts')),
                ('EARN_TRANS_ID', models.ForeignKey(db_column='EARN_TRANS_ID', null=True, on_delete=django.db.models.deletion.SET_NULL, to='finance.earning_transactions')),
                ('EXPNS_TRANS_ID', models.ForeignKey(db_column='EXPNS_TRANS_ID', null=True, on_delete=django.db.models.deletion.SET_NULL, to='finance.expense_transactions')),
            ],
            options={
                'db_table': 'ACCT_LEDGER',
            },
        ),
    ]