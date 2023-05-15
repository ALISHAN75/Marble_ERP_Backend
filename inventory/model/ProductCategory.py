from django.db import models


class ProductCategory(models.Model):

    CAT_ID = models.AutoField(
        primary_key=True,
        null=False,
        blank=False
    )

    CAT_NM = models.CharField(
        max_length=45,
        unique=True
    )

    CAT_NM_UR = models.CharField(
        max_length=45,
        unique=True,
        blank=True,
        null=True
        
    )

    CAT_DESC = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    CAT_DESC_UR = models.CharField(
        max_length=100,
        blank=True,
        null=True
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

        db_table = 'product_category'
