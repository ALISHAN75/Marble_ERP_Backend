from django.db import models
from rest_framework.validators import UniqueValidator
#  models
from inventory.model.ProductSizes import ProductSizes


class UsageType(models.Model):

    USAGE_ID = models.AutoField(
        primary_key=True,
        null=False,
        blank=False
    )

    USAGE_NM = models.CharField(
        max_length=45,
        unique=True
    )

    USAGE_NM_UR = models.CharField(
        max_length=45,
        unique=True,
        blank=True,
        null=True
    )

    USAGE_DESC = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    USAGE_DESC_UR = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    # SIZES =  models.ManyToManyField(ProductSizes)

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

        db_table = 'usage_type'
