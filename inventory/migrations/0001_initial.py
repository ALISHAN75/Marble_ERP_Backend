# Generated by Django 4.1.2 on 2022-10-26 05:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('hrm', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory_Transactions',
            fields=[
                ('INV_TRANS_ID', models.AutoField(primary_key=True, serialize=False)),
                ('INVNTRY_DT', models.DateField()),
                ('TRANS_TYP', models.CharField(max_length=45)),
                ('LABOUR_COST', models.DecimalField(decimal_places=2, max_digits=10)),
                ('LABOUR_SQFT', models.DecimalField(decimal_places=2, max_digits=10)),
                ('LABOUR_RUN_FT', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('TRANS_UNIT_COST', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('REC_ADD_DT', models.DateTimeField(auto_now_add=True)),
                ('REC_ADD_BY', models.IntegerField()),
                ('ACCT_ID', models.ForeignKey(db_column='ACCT_ID', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='inv_acct_id', to='accounts.accounts')),
            ],
            options={
                'db_table': 'INVENTORY_TRANSACTIONS',
            },
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('CAT_ID', models.AutoField(primary_key=True, serialize=False)),
                ('CAT_NM', models.CharField(max_length=45, unique=True)),
                ('CAT_DESC', models.CharField(blank=True, max_length=100, null=True)),
                ('IS_ACTIVE', models.IntegerField(default=1, null=True)),
                ('REC_ADD_DT', models.DateTimeField(auto_now_add=True)),
                ('REC_ADD_BY', models.IntegerField()),
                ('REC_MOD_DT', models.DateTimeField(auto_now=True)),
                ('REC_MOD_BY', models.IntegerField()),
            ],
            options={
                'db_table': 'PRODUCT_CATEGORY',
            },
        ),
        migrations.CreateModel(
            name='ProductName',
            fields=[
                ('PROD_NM_ID', models.AutoField(primary_key=True, serialize=False)),
                ('PROD_NM', models.CharField(max_length=45, unique=True)),
                ('PROD_NM_DESC', models.CharField(blank=True, max_length=100, null=True)),
                ('IS_ACTIVE', models.IntegerField(default=1, null=True)),
                ('REC_ADD_DT', models.DateTimeField(auto_now_add=True)),
                ('REC_ADD_BY', models.IntegerField()),
                ('REC_MOD_DT', models.DateTimeField(auto_now=True)),
                ('REC_MOD_BY', models.IntegerField()),
            ],
            options={
                'db_table': 'PRODUCT_NAME',
            },
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('PRODUCT_ID', models.AutoField(primary_key=True, serialize=False)),
                ('PROD_AVLBL_QTY', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('IS_ACTIVE', models.IntegerField(default=1, null=True)),
                ('REC_ADD_DT', models.DateTimeField(auto_now_add=True)),
                ('REC_ADD_BY', models.IntegerField()),
                ('REC_MOD_DT', models.DateTimeField(auto_now=True)),
                ('REC_MOD_BY', models.IntegerField()),
                ('CAT_ID', models.ForeignKey(db_column='CAT_ID', on_delete=django.db.models.deletion.CASCADE, related_name='prod_cat_id', to='inventory.productcategory')),
                ('PROD_NM_ID', models.ForeignKey(db_column='PROD_NM_ID', on_delete=django.db.models.deletion.CASCADE, related_name='prod_nm_id', to='inventory.productname')),
            ],
            options={
                'db_table': 'PRODUCTS',
            },
        ),
        migrations.CreateModel(
            name='ProductSizes',
            fields=[
                ('SIZE_ID', models.AutoField(primary_key=True, serialize=False)),
                ('WIDTH', models.DecimalField(decimal_places=2, max_digits=10)),
                ('LENGHT', models.DecimalField(decimal_places=2, max_digits=10)),
                ('THICKNESS', models.DecimalField(decimal_places=2, max_digits=10)),
                ('REC_ADD_DT', models.DateTimeField(auto_now_add=True)),
                ('REC_ADD_BY', models.IntegerField()),
                ('REC_MOD_DT', models.DateTimeField(auto_now=True)),
                ('REC_MOD_BY', models.IntegerField()),
            ],
            options={
                'db_table': 'PRODUCT_SIZES',
                'unique_together': {('WIDTH', 'LENGHT', 'THICKNESS')},
            },
        ),
        migrations.CreateModel(
            name='UsageType',
            fields=[
                ('USAGE_ID', models.AutoField(primary_key=True, serialize=False)),
                ('USAGE_NM', models.CharField(max_length=45, unique=True)),
                ('USAGE_DESC', models.CharField(blank=True, max_length=100, null=True)),
                ('IS_ACTIVE', models.IntegerField(default=1, null=True)),
                ('REC_ADD_DT', models.DateTimeField(auto_now_add=True)),
                ('REC_ADD_BY', models.IntegerField()),
                ('REC_MOD_DT', models.DateTimeField(auto_now=True)),
                ('REC_MOD_BY', models.IntegerField()),
            ],
            options={
                'db_table': 'USAGE_TYPE',
            },
        ),
        migrations.CreateModel(
            name='Transaction_Details',
            fields=[
                ('INV_TRANS_DETAIL_ID', models.AutoField(primary_key=True, serialize=False)),
                ('IS_LAST_REC', models.IntegerField(default=1)),
                ('QTY', models.DecimalField(decimal_places=2, max_digits=10)),
                ('QTY_SQFT', models.DecimalField(decimal_places=2, max_digits=10)),
                ('TOTAL_PROD_UNIT_COST', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('TOTAL_AVG_PROD_UNIT_COST', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('IS_SECTIONED', models.IntegerField()),
                ('IS_GOLA', models.IntegerField()),
                ('IS_SIZED', models.IntegerField()),
                ('IS_POLISHED', models.IntegerField()),
                ('IS_AVLBL', models.IntegerField()),
                ('AVLBL_QTY', models.DecimalField(decimal_places=2, max_digits=10)),
                ('AVLBL_SQFT', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('REC_ADD_DT', models.DateTimeField(auto_now_add=True)),
                ('REC_ADD_BY', models.IntegerField()),
                ('INV_TRANS_ID', models.ForeignKey(db_column='INV_TRANS_ID', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='inv_trans_id', to='inventory.inventory_transactions')),
                ('PROD_ID', models.ForeignKey(db_column='PROD_ID', null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.products')),
                ('SIZE_ID', models.ForeignKey(db_column='SIZE_ID', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='inv_size_id', to='inventory.productsizes')),
            ],
            options={
                'db_table': 'TRANSACTIONS_DETAILS',
            },
        ),
        migrations.CreateModel(
            name='ProductUsageSizes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PRODUCTSIZES_ID', models.ForeignKey(db_column='PRODUCTSIZES_ID', default=1, on_delete=django.db.models.deletion.CASCADE, to='inventory.productsizes')),
                ('USAGETYPE_ID', models.ForeignKey(db_column='USAGETYPE_ID', default=1, on_delete=django.db.models.deletion.CASCADE, to='inventory.usagetype')),
            ],
        ),
        migrations.AddField(
            model_name='products',
            name='USAGE_ID',
            field=models.ForeignKey(db_column='USAGE_ID', on_delete=django.db.models.deletion.CASCADE, related_name='prod_usage_id', to='inventory.usagetype'),
        ),
        migrations.CreateModel(
            name='ProductInventory',
            fields=[
                ('INV_PROD_ID', models.AutoField(primary_key=True, serialize=False)),
                ('IS_SECTIONED', models.IntegerField()),
                ('IS_GOLA', models.IntegerField()),
                ('IS_SIZED', models.IntegerField()),
                ('IS_POLISHED', models.IntegerField()),
                ('IS_AVLBL', models.IntegerField()),
                ('QTY', models.DecimalField(decimal_places=2, max_digits=10)),
                ('QTY_SQFT', models.DecimalField(decimal_places=2, max_digits=10)),
                ('AVLBL_QTY', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('AVLBL_SQFT', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('TOTAL_PROD_UNIT_COST', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('TOTAL_AVG_PROD_UNIT_COST', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('REC_ADD_DT', models.DateTimeField(auto_now_add=True)),
                ('REC_ADD_BY', models.IntegerField()),
                ('REC_MOD_DT', models.DateTimeField(auto_now=True)),
                ('REC_MOD_BY', models.IntegerField()),
                ('PROD_ID', models.ForeignKey(db_column='PROD_ID', null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.products')),
                ('SIZE_ID', models.ForeignKey(db_column='SIZE_ID', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pi_size_id', to='inventory.productsizes')),
            ],
            options={
                'db_table': 'PRODUCTS_INVENTORY',
            },
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('ORDR_ID', models.AutoField(primary_key=True, serialize=False)),
                ('ORDR_NO', models.CharField(max_length=45)),
                ('DELVRY_STS', models.IntegerField()),
                ('IS_SALE', models.IntegerField()),
                ('ORDR_DT', models.DateField()),
                ('ORDR_TOTAL_wTAX', models.DecimalField(decimal_places=2, max_digits=10)),
                ('TAX_PRCNT', models.DecimalField(decimal_places=2, max_digits=10)),
                ('ORDR_TOTAL_no_TAX', models.DecimalField(decimal_places=2, max_digits=10)),
                ('ORDER_DETAIL', models.CharField(blank=True, max_length=100)),
                ('IS_ACTIVE', models.IntegerField(default=1)),
                ('REC_ADD_DT', models.DateTimeField(auto_now_add=True)),
                ('REC_ADD_BY', models.IntegerField()),
                ('REC_MOD_DT', models.DateTimeField(auto_now=True)),
                ('REC_MOD_BY', models.IntegerField()),
                ('CUST_ACCT_ID', models.ForeignKey(db_column='CUST_ACCT_ID', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rn_cust_acct_id', to='accounts.accounts')),
                ('MRCHNT_ACCT_ID', models.ForeignKey(db_column='MRCHNT_ACCT_ID', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rn_merchnt_acct_id', to='accounts.accounts')),
                ('ORDR_BY_EMP_ID', models.ForeignKey(db_column='ORDR_BY_EMP_ID', null=True, on_delete=django.db.models.deletion.SET_NULL, to='hrm.employee')),
            ],
            options={
                'db_table': 'ORDERS',
            },
        ),
        migrations.CreateModel(
            name='Order_items',
            fields=[
                ('ORDR_ITEM_ID', models.AutoField(primary_key=True, serialize=False)),
                ('REQ_QTY', models.DecimalField(decimal_places=2, max_digits=10)),
                ('PAY_QTY', models.DecimalField(decimal_places=2, max_digits=10)),
                ('REQ_SQFT', models.DecimalField(decimal_places=2, max_digits=10)),
                ('PAY_SQFT', models.DecimalField(decimal_places=2, max_digits=10)),
                ('PROD_UNIT_COST', models.DecimalField(decimal_places=2, max_digits=10)),
                ('PROD_TOTL_PRICE', models.DecimalField(decimal_places=2, max_digits=10)),
                ('PROD_DESC', models.CharField(blank=True, max_length=100, null=True)),
                ('IS_SECTIONED', models.IntegerField()),
                ('IS_GOLA', models.IntegerField()),
                ('IS_SIZED', models.IntegerField()),
                ('IS_POLISHED', models.IntegerField()),
                ('IS_DLVRD', models.IntegerField(default=0)),
                ('DLVRD_QTY', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('REC_ADD_DT', models.DateTimeField(auto_now_add=True)),
                ('REC_ADD_BY', models.IntegerField(blank=True, null=True)),
                ('REC_MOD_DT', models.DateTimeField(auto_now=True)),
                ('REC_MOD_BY', models.IntegerField(blank=True, null=True)),
                ('DLVRY_SIZE_ID', models.ForeignKey(db_column='DLVRY_SIZE_ID', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='oi_req_size_id', to='inventory.productsizes')),
                ('ORDR_ID', models.ForeignKey(db_column='ORDR_ID', null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.orders')),
                ('PAY_SIZE_ID', models.ForeignKey(db_column='PAY_SIZE_ID', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='oi_pay_size_id', to='inventory.productsizes')),
                ('PRODUCT_ID', models.ForeignKey(db_column='PRODUCT_ID', null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.products')),
            ],
            options={
                'db_table': 'ORDER_ITEMS',
            },
        ),
        migrations.CreateModel(
            name='Breakage',
            fields=[
                ('BREAK_ID', models.AutoField(primary_key=True, serialize=False)),
                ('AVLBL_QTY', models.DecimalField(decimal_places=2, max_digits=10)),
                ('AVLBL_SQFT', models.DecimalField(decimal_places=2, max_digits=10)),
                ('REC_ADD_DT', models.DateTimeField(auto_now_add=True)),
                ('REC_ADD_BY', models.IntegerField()),
                ('REC_MOD_DT', models.DateTimeField(auto_now=True)),
                ('REC_MOD_BY', models.IntegerField()),
                ('INV_TRANS_ID', models.ForeignKey(db_column='INV_TRANS_ID', on_delete=django.db.models.deletion.CASCADE, related_name='break_trans_id', to='inventory.inventory_transactions')),
                ('PROD_ID', models.ForeignKey(db_column='PROD_ID', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='break_prod_id', to='inventory.products')),
            ],
            options={
                'db_table': 'BREAKAGE',
            },
        ),
        migrations.AlterUniqueTogether(
            name='products',
            unique_together={('PROD_NM_ID', 'CAT_ID', 'USAGE_ID')},
        ),
    ]