from django.db import models
from hrm.model.Employee_Departments import Employee_Departments


class Employee_Designations(models.Model):

    EMP_DESIG_ID = models.AutoField(
        primary_key=True,
        null=False,
        blank=True
    )

    DESIG_NM = models.CharField(
        max_length=45,
        unique=True,
    )

    DESIG_NM_UR = models.CharField(
        max_length=45,
        null=True,
        blank=True,
        unique=True,
    )

    DESIG_DESC = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    DESIG_DESC_UR = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    IS_ACTIVE = models.IntegerField(
        null=False,
        default=1
    )

    EMP_DEPT_ID = models.ForeignKey(
        Employee_Departments,
        on_delete=models.CASCADE, db_column="EMP_DEPT_ID")

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

    @property
    def EMP_DEPT(self):
        return self.EMP_DEPT_ID

    class Meta:

        # db_table = 'EMPLOYEE_DESIGNATIONS'
        db_table = 'employee_designations'
