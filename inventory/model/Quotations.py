from django.db import models
#  models
from hrm.model.Employee import Employee
from accounts.model.Account import Accounts
from inventory.model.ProductSizes import ProductSizes
from inventory.model.Products import Products


class Quotations(models.Model):

    QUOTE_ID = models.AutoField(
        primary_key=True,
        null=False,
        blank=False
    )


    DELVRY_STS = models.IntegerField(
        null=False,
        default=0
    )

    ADV_PAYMENT  = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        default=0
    )

    IS_SALE = models.IntegerField(
        null=False,
        default=1
    )

    ORDR_DT = models.DateField(
        null=False,
        blank=False,
    )

    ORDR_TOTAL_wTAX = models.DecimalField(
        null=False,
        max_digits=10,
        decimal_places=2,

    )

    TAX_PRCNT = models.DecimalField(
        null=False,
        max_digits=10,
        decimal_places=2,

    )

    ORDR_TOTAL_no_TAX = models.DecimalField(
        null=False,
        max_digits=10,
        decimal_places=2,

    )

    ORDER_DETAIL = models.CharField(
        max_length=100,
        blank=True,
        null=False,
    )

    ORDER_DETAIL_UR = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    ORDR_BY_EMP_ID = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        db_column="ORDR_BY_EMP_ID",
        related_name="q_by_emp_id",
        null=True

    )

    MRCHNT_ACCT_ID = models.ForeignKey(
        Accounts,
        on_delete=models.SET_NULL,
        related_name="q_merchnt_acct_id",
        db_column="MRCHNT_ACCT_ID",
        null=True

    )

    CUST_ACCT_ID = models.ForeignKey(
        Accounts,
        on_delete=models.SET_NULL,
        related_name="q_cust_acct_id",
        db_column="CUST_ACCT_ID",
        null=True

    )

    IS_ACTIVE = models.IntegerField(
        default=0,
        null=False,
    )

    REC_ADD_DT = models.DateTimeField(
        null=False,
        auto_now_add=True,
    )

    REC_ADD_BY = models.IntegerField(
        null=False,
        blank=False,
    )

    REC_MOD_DT = models.DateTimeField(
        null=False,
        auto_now=True,
    )

    REC_MOD_BY = models.IntegerField(
        null=False,
        blank=False,
    )


    EXPIRY_DT = models.DateField(
        null=True
    )

    IS_NOW_ORDER = models.IntegerField(
        default=0,
        null=False,
    )

    CUST_NM = models.CharField(
        max_length=100,
        blank=True,
        null=False,
    )

    CUST_NM_UR = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )


    CUST_PHONE = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    @property
    def ORDER_ITEMS(self):
        return Quotations_Items.objects.filter(QUOTE_ID=self.QUOTE_ID)

    class Meta:

        db_table = 'quotations'


class Quotations_Items(models.Model):

    QUOTE_ITEM_ID = models.AutoField(
        primary_key=True,
        null=False,
        blank=False
    )

    REQ_QTY = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
    )

    PAY_QTY = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
    )

    REQ_SQFT = models.DecimalField(
        max_digits=10,
        decimal_places=2,

        null=True,
    )

    IS_ACTIVE = models.IntegerField(
        default=1,
        null=False,
    )

    PAY_SQFT = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
    )

    PROD_UNIT_COST = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
    )

    PROD_TOTL_PRICE = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
    )

    PROD_DESC = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    PROD_DESC_UR = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    IS_SECTIONED = models.IntegerField(
        null=True,
    )

    IS_GOLA = models.IntegerField(
        null=True,
    )

    IS_SIZED = models.IntegerField(
        null=True,
    )

    IS_POLISHED = models.IntegerField(
        null=True,
    )

    IS_DLVRD = models.IntegerField(
        null=True,
        default=0

    )

    DLVRD_QTY = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        default=0
    )

    QUOTE_ID = models.ForeignKey(
        Quotations,
        on_delete=models.SET_NULL, db_column="QUOTE_ID",
        null=True,

    )

    PRODUCT_ID = models.ForeignKey(
        Products,
        on_delete=models.SET_NULL, db_column="PRODUCT_ID",
        null=True
    )

    DLVRY_SIZE_ID = models.ForeignKey(
        ProductSizes,
        on_delete=models.SET_NULL,
        db_column="DLVRY_SIZE_ID",
        related_name="q_req_size_id",
        null=True

    )

    PAY_SIZE_ID = models.ForeignKey(
        ProductSizes,
        on_delete=models.SET_NULL,
        db_column="PAY_SIZE_ID",
        related_name="q_pay_size_id",
        null=True

    )

    REC_ADD_DT = models.DateTimeField(
        auto_now_add=True,
        null=False,
    )

    REC_ADD_BY = models.IntegerField(
        blank=True,
        null=True,
    )

    REC_MOD_DT = models.DateTimeField(
        auto_now=True,
        null=False,
    )

    REC_MOD_BY = models.IntegerField(
        blank=True,
        null=True,
    )

    IS_GEN_PROD = models.IntegerField(
        null=False,
        default=0
    )

    GEN_PROD_NM = models.CharField(
        null=True,
        blank=True,
        max_length=45,
    )


    GEN_PROD_NM_UR = models.CharField(
        null=True,
        blank=True,
        max_length=45,
    )

    class Meta:

        db_table = 'quotations_items'
