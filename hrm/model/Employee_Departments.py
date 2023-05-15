from django.db import models


class Employee_Departments(models.Model):

    EMP_DEPT_ID = models.AutoField(
        primary_key=True,
        null=False,
        blank=False
    )

    DEPT_NM = models.CharField(
        max_length=45,
        null=False
    )

    DEPT_NM_UR = models.CharField(
        max_length=45,
        null=True
    )

    DEPT_DESC = models.CharField(
        max_length=100,
        null=True
    )

    DEPT_DESC_UR = models.CharField(
        max_length=100,
        null=True
    )

    IS_ACTIVE = models.IntegerField(
        null=False,
        default=1
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

    # def __str__(self):
    #     return self.EMP_DEPT_ID

    class Meta:

        # db_table = 'EMPLOYEE_DEPARTMENTS'
        db_table = 'employee_departments'
