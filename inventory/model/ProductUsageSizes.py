from django.db import models
# models
from inventory.model.ProductSizes import ProductSizes
from inventory.model.UsageType import UsageType


class ProductUsageSizes(models.Model):

    USAGETYPE_ID = models.ForeignKey(
        UsageType, db_column="USAGETYPE_ID", on_delete=models.CASCADE, default=1)

    PRODUCTSIZES_ID = models.ForeignKey(
        ProductSizes, db_column="PRODUCTSIZES_ID", on_delete=models.CASCADE, default=1)

    # class Meta:
    #     db_table = 'products_usage_typ_id'
