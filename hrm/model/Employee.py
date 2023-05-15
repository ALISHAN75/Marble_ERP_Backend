from django.db import models
#  models
from hrm.model.Employee_Designations import Employee_Designations
from hrm.model.Employment_Types import Employment_Types
from accounts.model.Account import User, Accounts


class Employee(models.Model):

    EMP_ID = models.AutoField(
        primary_key=True,
        blank=False,
        null=False
    )

    EMP_FULL_NM = models.CharField(
        max_length=45,
        null=True,
        blank=True
    )

    EMP_FULL_NM_UR = models.CharField(
        max_length=45,
        null=True,
        blank=True
    )

    USER_ID = models.ForeignKey(
        User,
        on_delete=models.CASCADE, db_column="USER_ID",
        null=True
    )

    EMP_STRT_DT = models.DateTimeField(
        null=False,
        blank=False,
    )

    EMP_TERM_DT = models.DateTimeField(
        null=True,
        blank=True
    )

    EMP_STS = models.IntegerField(
        default=1
    )

    EMP_TERM_REASN = models.CharField(
        max_length=500,
        null=True,
        blank=True
    )

    EMP_TERM_REASN_UR = models.CharField(
        max_length=500,
        null=True,
        blank=True
    )

    EMP_DESIG_ID = models.ForeignKey(
        Employee_Designations,
        on_delete=models.CASCADE, db_column="EMP_DESIG_ID")

    EMP_TYP_ID = models.ForeignKey(
        Employment_Types,
        on_delete=models.CASCADE, db_column="EMP_TYP_ID")

    CNIC = models.CharField(
        max_length=45,
        null=True,
        blank=True
    )

    CNIC_EXP_DT = models.DateField(
        null=True,
        blank=True
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

    @property
    def USER(self):
        return self.USER_ID

    @property
    def EMP_TYPE(self):
        return self.EMP_TYP_ID

    @property
    def EMP_DESIG(self):
        return self.EMP_DESIG_ID

    @property
    def EMP_COMPENSATION(self):
        return Employee_Compensation.objects.filter(EMP_ID=self.EMP_ID)

    @property
    def ACCOUNT(self):
        return Accounts.objects.get(USER_ID=self.USER_ID)

    class Meta:

        db_table = 'employees'


class Employee_Compensation(models.Model):

    EMP_CMPNSTN_ID = models.AutoField(
        primary_key=True,
        blank=False,
        null=False
    )

    COMPNSTN_AMNT = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False
    )

    COMPNSTN_UNIT_UR = models.CharField(
        max_length=45,
        blank=True,
        null= True
    )

    COMPNSTN_UNIT = models.CharField(
        max_length=45,
        blank=True,
        null= True
    )

    EFFCT_STRT_DT = models.DateField(
        null=True
    )

    EFFCT_END_DT = models.DateField(
        null=True
    )

    PAY_FREQ_TYP = models.CharField(
        max_length=45,
        blank=False,
        null=False,
    )

    PAY_FREQ_TYP_UR = models.CharField(
        max_length=45,
        blank=True,
        null= True
    )

    EMP_ID = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        db_column="EMP_ID",
        null=True
    )

    REC_ADD_DT = models.DateTimeField(
        auto_now_add=True
    )

    REC_ADD_BY = models.IntegerField(
        blank=True,
        null=True,
    )

    REC_MOD_DT = models.DateTimeField(
        auto_now=True
    )

    REC_MOD_BY = models.IntegerField(
        blank=True,
        null=True,
    )

    class Meta:

        # db_table = 'EMPLOYEE_COMPENSATION'
        db_table = 'employee_compensation'
