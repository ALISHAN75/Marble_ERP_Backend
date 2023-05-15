from email.policy import default
from django.db import models
# models
from inventory.model.ProductCategory import ProductCategory
from inventory.model.ProductName import ProductName
from inventory.model.UsageType import UsageType


class Products(models.Model):

    PRODUCT_ID = models.AutoField(
        primary_key=True,
        null=False,
        blank=False
    )

    PROD_NM_ID = models.ForeignKey(
        ProductName,
        on_delete=models.CASCADE,
        db_column="PROD_NM_ID",
        related_name="prod_nm_id"
    )

    CAT_ID = models.ForeignKey(
        ProductCategory,
        on_delete=models.CASCADE,
        db_column="CAT_ID",
        related_name="prod_cat_id"
    )

    USAGE_ID = models.ForeignKey(
        UsageType,
        on_delete=models.CASCADE,
        db_column="USAGE_ID",
        related_name="prod_usage_id"
    )

    PROD_AVLBL_QTY = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        default=0
    )

    IS_ACTIVE = models.IntegerField(
        default=1,
        null=True
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

        db_table = 'products'
        unique_together = ('PROD_NM_ID', 'CAT_ID', 'USAGE_ID',)
