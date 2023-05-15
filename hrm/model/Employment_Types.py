from django.db import models


class Employment_Types(models.Model):

    EMP_TYP_ID = models.AutoField(
        primary_key=True,
        null=False,
        blank=False
    )

    EMP_TYP_NM = models.CharField(
        max_length=45,
        null=False,
    )

    EMP_TYP_DESC = models.CharField(
        max_length=100
    
    )
    EMP_TYP_NM_UR = models.CharField(
        max_length=45,
        null=True,
    )

    EMP_TYP_DESC_UR = models.CharField(
        max_length=100,
        null=True,
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

        # db_table = 'EMPLOYMENT_TYPE'
        db_table = 'employment_type'
