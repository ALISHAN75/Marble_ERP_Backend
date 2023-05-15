from django.db import models
from accounts.model.Account import Accounts
# from accounts.model. import Accounts
from inventory.model.Inventory import Inventory_Transactions
from logistics.model.Deliveries import Deliveries
from hrm.model.Employee import Employee


class Earning_Transactions(models.Model):

    EARN_TRANS_ID = models.AutoField(
        primary_key=True,
        null=False,
        blank=False
    )

    PYMNT_BY_UR = models.CharField(
        max_length=100,
        null=True,
        blank=True
    
    )
    PYMNT_BY = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    PYMNT_AMNT = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False
    )

    PYMNT_DT = models.DateField(
        null=True
    )

    IS_CASH = models.IntegerField(
        default=0,
        null=True
    )

    NOTES = models.CharField(
        max_length=300,
        null=True,
        blank=True
    
    )
    NOTES_UR = models.CharField(
        max_length=300,
        null=True,
        blank=True
    )

    ACCT_ID = models.ForeignKey(
        Accounts,
        on_delete=models.SET_NULL,
        db_column="ACCT_ID",
        null=True
    )

    EMP_ID = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        db_column="EMP_ID",
        null=True
    )

    DLVRY_ID = models.ForeignKey(
        Deliveries,
        on_delete=models.SET_NULL,
        db_column="DLVRY_ID",
        null=True
    )

    EARN_TYP_ACCT = models.ForeignKey(
        Accounts,
        on_delete=models.SET_NULL,
        db_column="EARN_TYP_ACCT",
        related_name='earn_typ_acct',
        null=True
    )

    INVNTRY_TRANS_ID = models.ForeignKey(
        Inventory_Transactions,
        on_delete=models.SET_NULL,
        db_column="INVNTRY_TRANS_ID",
        null=True
    )

    REC_ADD_DT = models.DateTimeField(
        auto_now_add=True
    )

    REC_ADD_BY = models.IntegerField(
        blank=True,
        null=True,
    )

    @property
    def EARNS_TRANS_ITEMS(self):
        return Earning_Transaction_Items.objects.filter(EARN_TRANS_ID=self.EARN_TRANS_ID)

    class Meta:

        # db_table = 'EARNING_TRANSACTIONS'
        db_table = 'earning_transactions'


# Earning Transaction Items
class Earning_Transaction_Items(models.Model):

    EARN_TRANS_ITEM_ID = models.AutoField(
        primary_key=True,
        null=False,
        blank=False
    )

    EARN_TRANS_ID = models.ForeignKey(
        Earning_Transactions,
        on_delete=models.SET_NULL,
        db_column="EARN_TRANS_ID",
        null=True
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

    ITEM_UNIT_AMNT = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
    )

    ITEM_UNIT_QUANTITY = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,

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

        # db_table = 'EARNING_TRANSACTION_ITEMS'
        db_table = 'earning_transaction_items'
