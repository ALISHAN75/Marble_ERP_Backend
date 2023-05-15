from django.db import models
from inventory.model.ProductSizes import ProductSizes
from inventory.model.Products import Products
from inventory.model.Inventory import Transaction_Details


class ProductInventory(models.Model):

    INV_PROD_ID = models.AutoField(
        primary_key=True,
        null=False,
        blank=False
    )

    # INV_TRANS_DETAIL_ID = models.ForeignKey(
    #     Transaction_Details,
    #     on_delete=models.SET_NULL,
    #     db_column="transac-detail_id",
    #     null=True
    # )

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
        related_name="pi_size_id",
        null=True
    )

    IS_SECTIONED = models.IntegerField()

    IS_GOLA = models.IntegerField()

    IS_SIZED = models.IntegerField()

    IS_POLISHED = models.IntegerField()

    IS_AVLBL = models.IntegerField()

    QTY = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    QTY_SQFT = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    AVLBL_QTY = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    AVLBL_SQFT = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
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

    REC_ADD_DT = models.DateTimeField(
        auto_now_add=True
    )

    REC_ADD_BY = models.IntegerField(
        blank=False,
        null=False,
    )

    REC_MOD_DT = models.DateTimeField(
        auto_now=True
    )

    REC_MOD_BY = models.IntegerField(
        blank=False,
        null=False,
    )

    class Meta:

        db_table = 'products_inventory'
