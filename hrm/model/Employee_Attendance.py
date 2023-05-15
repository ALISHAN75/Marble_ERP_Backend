from django.db import models

from hrm.model.Employee import Employee


class Employee_Attendance(models.Model):

    EMP_ATTND_ID = models.AutoField(
        primary_key=True,
        blank=False,
        null=False
    )

    EMP_ID = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        db_column="EMP_ID"
    )

    EMP_ATTND_DT = models.DateField()

    EMP_ATTND_STS = models.IntegerField(
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

    def EMP(self):
        return self.EMP_ID

    class Meta:

        # db_table = 'EMPLOYEE_ATTENDANCE'
        db_table = 'employee_attendance'


