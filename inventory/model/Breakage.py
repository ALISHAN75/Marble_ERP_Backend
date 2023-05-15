from django.db import models
# models
from inventory.model.Inventory import Inventory_Transactions
from inventory.model.Products import Products

# Table: breakage
# Columns:
# BREAK_ID int(11) AI PK 
# AVLBL_SQFT decimal(10,2) 
# REC_ADD_DT datetime(6) 
# REC_ADD_BY int(11) 
# INV_TRANS_ID int(11) 
# PROD_ID int(11)

class Breakage(models.Model):

    BREAK_ID = models.AutoField(
        primary_key=True,
        null=False,
        blank=False
    )

    PROD_ID = models.ForeignKey(
        Products,
        on_delete=models.SET_NULL,
        db_column="PROD_ID",
        related_name="break_prod_id",
        null=True
    )

    AVLBL_SQFT = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    INV_TRANS_ID = models.ForeignKey(
        Inventory_Transactions,
        on_delete=models.CASCADE,
        db_column="INV_TRANS_ID",
        related_name="break_trans_id"
    )

    REC_ADD_DT = models.DateTimeField(
        auto_now_add=True
    )

    REC_ADD_BY = models.IntegerField(
        blank=False,
        null=False,
    )

    class Meta:

        db_table = 'breakage'