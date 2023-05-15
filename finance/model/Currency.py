from django.db import models


class Currency(models.Model):

    CURNCY_ID = models.AutoField(
        primary_key=True,
        null=False,
        blank=False
    )

    ISO_CODE = models.CharField(
        max_length=5,
        null=False,
        blank=False
    )

    SIGN = models.CharField(
        max_length=5,
        null=False,
        blank=False
    )

    COUNTRY = models.CharField(
        max_length=100,
        null=False,
        blank=False
    )

    CURENCY_NAME = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    COUNTRY_CODE_CNTRY_ABB = models.CharField(
        max_length=2,
        null=True,
        blank=True
    )

    class Meta:

        # db_table = 'CURRENCY'
        db_table = 'currency'
