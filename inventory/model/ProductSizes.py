
# from django.db import models
# class Person(models.Model):
#     name = models.CharField(max_length=128)
# class Group(models.Model):
#     name = models.CharField(max_length=128)
#     persons = models.ManyToManyField(Person, through='Membership')

from django.db import models


class ProductSizes(models.Model):

    SIZE_ID = models.AutoField(
        primary_key=True,
        null=False,
        blank=False
    )

    WIDTH = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False
    )

    LENGTH = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False
    )

    THICKNESS = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False
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
        db_table = 'product_sizes'
        unique_together = ('WIDTH', 'LENGTH', 'THICKNESS',)
