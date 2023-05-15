from django.db import models
from accounts.model.Account import Accounts
# from inventory.model.TransactionDetails import Transaction_Details
from inventory.model.ProductSizes import ProductSizes
from inventory.model.Products import Products


class Inventory_Transactions(models.Model):

    INV_TRANS_ID = models.AutoField(
        primary_key=True,
        null=False,
        blank=False
    )

    INVNTRY_DT = models.DateField()

    TRANS_TYP = models.CharField(max_length=45)

    TRANS_TYP_UR = models.CharField(max_length=45,null=True,blank=True)

    LABOUR_COST = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    LABOUR_SQFT = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    LABOUR_RUN_FT = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    TRANS_UNIT_COST = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    ACCT_ID = models.ForeignKey(
        Accounts,
        on_delete=models.SET_NULL,
        db_column="ACCT_ID",
        related_name="inv_acct_id",
        null=True
    )

    REC_ADD_DT = models.DateTimeField(
        auto_now_add=True
    )

    REC_ADD_BY = models.IntegerField(
        blank=False,
        null=False,
    )

    @property
    def TRANSC_DETALS(self):
        return Transaction_Details.objects.filter(INV_TRANS_ID=self.INV_TRANS_ID)

    class Meta:

        db_table = 'inventory_transactions'


class Transaction_Details(models.Model):

    INV_TRANS_DETAIL_ID = models.AutoField(
        primary_key=True,
        null=False,
        blank=False
    )

    IS_LAST_REC = models.IntegerField(
        default=1
    )

    QTY = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    QTY_SQFT = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    TOTAL_PROD_UNIT_COST = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    TOTAL_AVG_PROD_UNIT_COST = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    IS_SECTIONED = models.IntegerField()

    IS_GOLA = models.IntegerField()

    IS_SIZED = models.IntegerField()

    IS_POLISHED = models.IntegerField()

    IS_AVLBL = models.IntegerField()

    AVLBL_QTY = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    AVLBL_SQFT = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    PROD_ID = models.ForeignKey(
        Products,
        on_delete=models.SET_NULL,
        db_column="PROD_ID",
        null=True
    )

    SIZE_ID = models.ForeignKey(
        ProductSizes,
        on_delete=models.SET_NULL,
        db_column="SIZE_ID",
        related_name="inv_size_id",
        null=True
    )

    INV_TRANS_ID = models.ForeignKey(
        Inventory_Transactions,
        on_delete=models.SET_NULL,
        db_column="INV_TRANS_ID",
        related_name="inv_trans_id",
        null=True
    )

    REC_ADD_DT = models.DateTimeField(
        auto_now_add=True
    )

    REC_ADD_BY = models.IntegerField(
        blank=False,
        null=False,
    )

    class Meta:

        db_table = 'transactions_details'
