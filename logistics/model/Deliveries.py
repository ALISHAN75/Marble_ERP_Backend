from email.policy import default
from modulefinder import LOAD_CONST
from django.db import models
#   models
from hrm.model.Employee import Employee
from accounts.model.Account import Accounts
from inventory.model.Orders import Order_items, Orders
from inventory.model.Products import Products


class Deliveries(models.Model):

    DLVRY_ID = models.AutoField(
        primary_key=True,
        null=False,
        blank=False
    )

    DLVRY_DT = models.DateField(null=True)

    IS_SALE = models.IntegerField()

    IS_RETURN = models.IntegerField(
        default=0
    )

    SRC_ADDR = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    SRC_ADDR_UR = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    DESTNTN_ADDR = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    DESTNTN_ADDR_UR = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    DLVRY_DRIVER = models.CharField(
        max_length=45,
        blank=True,
        null=True
    )

    DLVRY_DRIVER_UR = models.CharField(
        max_length=45,
        blank=True,
        null=True
    )

    DRIVER_PH_NUM = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    DLVRY_VHICLE = models.CharField(
        max_length=45,
        blank=True,
        null=True
    )

    DLVRY_VHICLE_UR = models.CharField(
        max_length=45,
        blank=True,
        null=True
    )

    LOAD_COST = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    RENT_COST = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    EXTRAS_COST = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    DLVRY_COST = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    DLVRY_ORDR_COST = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    DLVRY_wORDR_COST = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    DLVRY_DETAIL = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    DLVRY_DETAIL_UR = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    DLVRY_BY_EMP_ID = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        db_column="DLVRY_BY_EMP_ID",
        null=True
    )

    CUST_ACCT_ID = models.ForeignKey(
        Accounts,
        on_delete=models.SET_NULL,
        related_name="lg_cust_acct_id",
        db_column="CUST_ACCT_ID",
        null=True
    )

    MRCHNT_ACCT_ID = models.ForeignKey(
        Accounts,
        on_delete=models.SET_NULL,
        db_column="MRCHNT_ACCT_ID",
        related_name="lg_merchnt_acct_id",
        null=True
    )

    ORDR_ID = models.ForeignKey(
        Orders,
        on_delete=models.CASCADE,
        db_column="ORDR_ID",
        related_name="lg_ordr_id",
    )

    IS_ACTIVE = models.IntegerField(
        default=1
    )

    REC_ADD_DT = models.DateTimeField(
        auto_now_add=True
    )

    REC_ADD_BY = models.IntegerField(
        blank=False,
        null=False,
        default=1
    )

    REC_MOD_DT = models.DateTimeField(
        auto_now=True
    )

    REC_MOD_BY = models.IntegerField(
        blank=False,
        null=False,
        default=1
    )

    @property
    def DELIVERY_ITEMS(self):
        return Delivery_Items.objects.filter(DLVRY_ID=self.DLVRY_ID)

    class Meta:

        db_table = 'deliveries'


class Delivery_Items(models.Model):

    DLVRY_ITEM_ID = models.AutoField(
        primary_key=True,
        null=False,
        blank=False
    )

    PROD_QTY = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    PROD_QTY_SQFT = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    UNIT_PRICE_noDLVRY = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    UNIT_DLVRY = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    UNIT_PRICE_wDLVRY = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    DLVRY_ITEM_TOTAL = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    DLVRY_ID = models.ForeignKey(
        Deliveries,
        on_delete=models.SET_NULL,
        db_column="DLVRY_ID",
        null=True
    )

    ORDR_ITEM_ID = models.ForeignKey(
        Order_items,
        on_delete=models.CASCADE,
        db_column="ORDR_ITEM_ID"
    )

    PRODUCT_ID = models.ForeignKey(
        Products,
        on_delete=models.CASCADE,
        db_column="PRODUCT_ID",
        related_name="lg_product_id",
        default=1
    )

    REC_ADD_DT = models.DateTimeField(
        auto_now_add=True
    )

    REC_ADD_BY = models.IntegerField(
        blank=True,
        null=True,
    )

    REC_MOD_DT = models.DateTimeField(
        auto_now=True
    )

    REC_MOD_BY = models.IntegerField(
        blank=True,
        null=True,
    )

    class Meta:

        db_table = 'delivery_items'
