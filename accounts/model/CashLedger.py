from django.db import models
# models
from accounts.model.Account import Accounts
from finance.model.Earning_Transactions import Earning_Transactions
from finance.model.Expense_Transactions import Expense_Transactions


class CashLedger(models.Model):

    ID = models.AutoField(
        primary_key=True,
        null=False,
        blank=False
    )

    ACCT_ID = models.ForeignKey(
        Accounts,
        on_delete=models.SET_NULL,
        db_column="ACCT_ID",
        null=True
    )

    ORDINAL = models.IntegerField(
        null=True,
        blank=True
    )

    TRANSC_DESC = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    TRANSC_DESC_UR = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    EARNING = models.FloatField(
        null=True
    )

    EXPENSE = models.FloatField(
        null=True
    )

    BALANCE = models.FloatField(
        null=True
    )

    REC_ADD_DT = models.DateTimeField(
        auto_now_add=True
    )

    REC_ADD_BY = models.IntegerField(
        blank=False,
        null=False,
        default=1
    )


    EARN_TRANS_ID = models.ForeignKey(
        Earning_Transactions,
        on_delete=models.SET_NULL, db_column="EARN_TRANS_ID",
        null=True 
    )

    EXPNS_TRANS_ID = models.ForeignKey(
        Expense_Transactions,
        on_delete=models.SET_NULL, db_column="EXPNS_TRANS_ID",
        null=True
    )


    @property
    def ACCOUNT(self):
        return self.ACCT_ID

    class Meta:

        # db_table = 'CASH_LEDGER'
        db_table = 'cash_ledger'
