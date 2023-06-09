# Generated by Django 4.1.2 on 2022-10-26 05:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventory', '0001_initial'),
        ('accounts', '0001_initial'),
        ('hrm', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deliveries',
            fields=[
                ('DLVRY_ID', models.AutoField(primary_key=True, serialize=False)),
                ('DLVRY_DT', models.DateField(null=True)),
                ('IS_SALE', models.IntegerField()),
                ('IS_RETURN', models.IntegerField(default=0)),
                ('SRC_ADDR', models.CharField(blank=True, max_length=100, null=True)),
                ('DESTNTN_ADDR', models.CharField(blank=True, max_length=100, null=True)),
                ('DLVRY_DRIVER', models.CharField(blank=True, max_length=45, null=True)),
                ('DLVRY_VHICLE', models.CharField(blank=True, max_length=45, null=True)),
                ('DLVRY_COST', models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True)),
                ('UNLOAD_COST', models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True)),
                ('DLVRY_DETAIL', models.CharField(blank=True, max_length=100, null=True)),
                ('IS_ACTIVE', models.IntegerField(default=1)),
                ('REC_ADD_DT', models.DateTimeField(auto_now_add=True)),
                ('REC_ADD_BY', models.IntegerField(default=1)),
                ('REC_MOD_DT', models.DateTimeField(auto_now=True)),
                ('REC_MOD_BY', models.IntegerField(default=1)),
                ('CUST_ACCT_ID', models.ForeignKey(db_column='CUST_ACCT_ID', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lg_cust_acct_id', to='accounts.accounts')),
                ('DLVRY_BY_EMP_ID', models.ForeignKey(db_column='DLVRY_BY_EMP_ID', null=True, on_delete=django.db.models.deletion.SET_NULL, to='hrm.employee')),
                ('MRCHNT_ACCT_ID', models.ForeignKey(db_column='MRCHNT_ACCT_ID', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lg_merchnt_acct_id', to='accounts.accounts')),
                ('ORDR_ID', models.ForeignKey(db_column='ORDR_ID', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lg_ordr_id', to='inventory.orders')),
            ],
            options={
                'db_table': 'DELIVERIES',
            },
        ),
        migrations.CreateModel(
            name='Delivery_Items',
            fields=[
                ('DLVRY_ITEM_ID', models.AutoField(primary_key=True, serialize=False)),
                ('PROD_QTY', models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True)),
                ('PROD_DESC', models.CharField(blank=True, max_length=100, null=True)),
                ('REC_ADD_DT', models.DateTimeField(auto_now_add=True)),
                ('REC_ADD_BY', models.IntegerField()),
                ('REC_MOD_DT', models.DateTimeField(auto_now=True)),
                ('REC_MOD_BY', models.IntegerField()),
                ('DLVRY_ID', models.ForeignKey(db_column='DLVRY_ID', null=True, on_delete=django.db.models.deletion.SET_NULL, to='logistics.deliveries')),
                ('ORDR_ITEM_ID', models.ForeignKey(db_column='ORDR_ITEM_ID', null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.order_items')),
                ('PRODUCT_ID', models.ForeignKey(db_column='PRODUCT_ID', null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.products')),
            ],
            options={
                'db_table': 'DELIVERY_ITEMS',
            },
        ),
    ]
