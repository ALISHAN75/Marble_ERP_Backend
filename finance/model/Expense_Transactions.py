from django.db import models
#  models
from accounts.model.Account import Accounts
from hrm.model.Employee import Employee
from logistics.model.Deliveries import Deliveries


class Expense_Transactions(models.Model):

    EXPNS_TRANS_ID = models.AutoField(
        primary_key=True,
        null=False,
        blank=False
    )

    PAYMNT_DT = models.DateField(
        null=True
    )

    EXPNS_TYP_ACCT = models.ForeignKey(
        Accounts,
        on_delete=models.SET_NULL,
        db_column="EXPNS_TYP_ACCT",
        related_name="expns_typ_acct",
        null=True
    )

    PYMENT_TO = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    PYMENT_TO_UR = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    PYMNT_AMNT = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False
    )

    IS_CASH = models.IntegerField(
        default=0,
        null=True
    )

    NOTES = models.CharField(
        max_length=500,
        null=True,
        blank=True
    )

    NOTES_UR = models.CharField(
        max_length=500,
        null=True,
        blank=True
    )

    ACCT_ID = models.ForeignKey(
        Accounts,
        on_delete=models.SET_NULL,
        db_column="ACCT_ID",
        related_name="acct_id",
        null=True
    )

    PYMNT_BY_EMP_ID = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        db_column="PYMNT_BY_EMP_ID",
        related_name="rn_salary_by_emp_id",
        null=True
    )

    DLVRY_ID = models.ForeignKey(
        Deliveries,
        on_delete=models.SET_NULL,
        db_column="DLVRY_ID",
        null=True
    )

    TAX_PRCNT = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        null=True
    )

    TOTAL_noTAX = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True
    )
    TOTAL_wTAX = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,

    )

    REC_ADD_DT = models.DateTimeField(
        auto_now_add=True
    )

    REC_ADD_BY = models.IntegerField(
        blank=True,
        null=True,
    )

    @property
    def EXPNS_TRANS_ITEMS(self):
        return Expense_Transaction_Items.objects.filter(EXPNS_TRANS_ID=self.EXPNS_TRANS_ID)

    class Meta:

        # db_table = 'EXPENSE_TRANSACTIONS'
        db_table = 'expense_transactions'


# Expense Transaction Items
class Expense_Transaction_Items(models.Model):

    EXPNS_TRANS_ITEM_ID = models.AutoField(
        primary_key=True,
        null=False,
        blank=False
    )

    EXPNS_TRANS_ID = models.ForeignKey(
        Expense_Transactions,
        on_delete=models.SET_NULL,
        db_column="EXPNS_TRANS_ID",
        null=True
    )

    ITEM_NM = models.CharField(
        max_length=45,
        null=False,
        blank=False,
    )

    ITEM_NM_UR = models.CharField(
        max_length=45,
        null=True,
    )

    ITEM_DESC = models.CharField(
        max_length=100,
        null=False,
        blank=False,    
    )

    ITEM_DESC_UR = models.CharField(
        max_length=100,
        null=True,    
    )

    ITEM_RATE_UNIT = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False
    )

    ITEM_UNIT_QUANTITY = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False
    )

    ITEM_TOTAL = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True
    )

    REC_ADD_DT = models.DateTimeField(
        auto_now_add=True
    )

    REC_ADD_BY = models.IntegerField(
        blank=True,
        null=True,
    )

    class Meta:

        # db_table = 'EXPENSE_TRANSACTION_ITEMS'
        db_table = 'expense_transaction_items'
