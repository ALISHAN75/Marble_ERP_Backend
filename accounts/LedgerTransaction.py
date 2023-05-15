# models imports
from accounts.model.Account import Accounts
from accounts.model.AcctLedger import Acct_Ledger
from accounts.model.CashLedger import CashLedger
# serializer imports
from accounts.serializer.CashLedgerSerializer import CashLedgerSerializer , AddCashLedgerSerializer
from accounts.serializer.UsersSerializer import AccountsSerializer
from accounts.serializer.AcctLedgerSerializer import AcctLedgerSerializer ,AddAcctLedgerSerializer
# utils
from finance.utiliy.FinanceUtil import FinanceUtil
from decimal import Decimal


class LedgerTransaction():

    def __init__(self, isExpense):
        self.isExpense = isExpense

    def getLedgerObj(self, transac , name):      
        ledger_obj = {}
        if self.isExpense is True:
          ledger_obj["TRANSC_DESC"] = "Expense" + "  " + str(transac.PYMNT_AMNT) + " to " + str(name)
          ledger_obj["EXPNS_TRANS_ID"] = transac.EXPNS_TRANS_ID
          ledger_obj["EXPENSE"] = transac.PYMNT_AMNT
        else:
          ledger_obj["TRANSC_DESC"] = "Earning" + "  " + str(transac.PYMNT_AMNT) + " from " + str(name)
          ledger_obj["EARN_TRANS_ID"] = transac.EARN_TRANS_ID
          ledger_obj["EARNING"] = transac.PYMNT_AMNT

        return ledger_obj
        # pass

    def getCashObj(self, transac):       
        cash_obj = {
            "ACCT_ID": transac.ACCT_ID.ACCT_ID
         }
        
        if self.isExpense is True:
          cash_obj["TRANSC_DESC"] = "Expense" + "  " + str(transac.PYMNT_AMNT) + " to " + str(transac.ACCT_ID.ACCT_TITLE)
          cash_obj["EXPNS_TRANS_ID"] = transac.EXPNS_TRANS_ID
          cash_obj["EXPENSE"] = transac.PYMNT_AMNT
        else:
          cash_obj["TRANSC_DESC"] = "Earning" + "  " + str(transac.PYMNT_AMNT) + " from " + str(transac.ACCT_ID.ACCT_TITLE)
          cash_obj["EARN_TRANS_ID"] = transac.EARN_TRANS_ID
          cash_obj["EARNING"] = transac.PYMNT_AMNT
        return cash_obj
        # pass

    # def getCashObj2(self, transac  ):
    #     cash_obj = {
    #       "ACCT_ID": transac.EARN_TYP_ACCT.ACCT_ID
    #     }
    #     if self.isExpense is True:
    #       cash_obj["EXPENSE"] = transac.PYMNT_AMNT
    #       cash_obj["TRANSC_DESC"] = "Expense" + " - " + str(transac.PYMNT_AMNT) + " to " + str(transac.EARN_TYP_ACCT.ACCT_TITLE)
    #     else:
    #       cash_obj["EARNING"] = transac.PYMNT_AMNT
    #       cash_obj["TRANSC_DESC"] = "Earning" + " - " + str(transac.PYMNT_AMNT) + " from " + str(transac.EARN_TYP_ACCT.ACCT_TITLE)
    #     return cash_obj
    #     # pass

    def findAccount(self, acct_id):
        # try:
        #   account_queryset = Accounts.objects.get(ACCT_ID=acct_id)
        #   return account_queryset
        # except Accounts.DoesNotExist:
        #   return None
        pass

    def updateAcctBalnce(self, account, updated_balance):
        account.CLOSNG_BLNCE = updated_balance
        account.save()
        pass

    def insertEarningTransac(self, account, ledger_obj, payment_amount):
        # ledger_obj["ACCT_ID"] = account.ACCT_ID

        # last_ledger_trans = Acct_Ledger.objects.filter(ACCT_ID= ledger_obj["ACCT_ID"]).order_by("-ORDINAL").first()
        # if last_ledger_trans:
        #   ledger_obj["BALANCE"] = float(last_ledger_trans.BALANCE) - float(payment_amount)
        #   ledger_obj["ORDINAL"] = last_ledger_trans.ORDINAL + 1
        # else:
        #   ledger_obj["BALANCE"] = float(account.CLOSNG_BLNCE) - float(payment_amount)
        #   ledger_obj["ORDINAL"] = 1

        # crt_acct_leg_serializer = AcctLedgerSerializer(data=ledger_obj)
        # crt_acct_leg_serializer.is_valid(raise_exception=True)
        # crt_acct_leg_serializer.save()
        # return crt_acct_leg_serializer
        pass

    def insertExpenseTransac(self, account, ledger_obj, payment_amount):
        # ledger_obj["ACCT_ID"] = account.ACCT_ID

        # last_ledger_trans = Acct_Ledger.objects.filter(ACCT_ID= ledger_obj["ACCT_ID"]).order_by("-ORDINAL").first()
        # if last_ledger_trans:
        #   ledger_obj["BALANCE"] = float(last_ledger_trans.BALANCE) + float(payment_amount)
        #   ledger_obj["ORDINAL"] = last_ledger_trans.ORDINAL + 1
        # else:
        #   ledger_obj["BALANCE"] = float(account.CLOSNG_BLNCE) + float(payment_amount)
        #   ledger_obj["ORDINAL"] = 1

        # crt_acct_leg_serializer = AcctLedgerSerializer(data=ledger_obj)
        # crt_acct_leg_serializer.is_valid(raise_exception=True)
        # crt_acct_leg_serializer.save()
        # return crt_acct_leg_serializer
        pass

    def insertEarning(self, account_id, earn_transac):
        # pass
        acct_to_update =  self.findCashAcct(acct_id=account_id)
        creat_ledger_obj =  self.getLedgerObj(transac=earn_transac , name = earn_transac.ACCT_ID.ACCT_TITLE )  
        creat_ledger_obj["ACCT_ID"] = acct_to_update.ACCT_ID
        # For Non-User Acoount      
        ern_type_acct_to_update =  self.findCashAcct(acct_id=earn_transac.EARN_TYP_ACCT.ACCT_ID)
        ern_type_creat_ledger_obj =  self.getLedgerObj(transac=earn_transac , name = earn_transac.EARN_TYP_ACCT.ACCT_TITLE)  
        ern_type_creat_ledger_obj["ACCT_ID"] = ern_type_acct_to_update.ACCT_ID

        payment_amount = earn_transac.PYMNT_AMNT
        # For Acoount
        last_ledger_trans = Acct_Ledger.objects.filter(ACCT_ID= creat_ledger_obj["ACCT_ID"]).order_by("-ORDINAL").first()
        if last_ledger_trans:
          creat_ledger_obj["BALANCE"] = float(last_ledger_trans.BALANCE) - float(payment_amount)
          creat_ledger_obj["ORDINAL"] = last_ledger_trans.ORDINAL + 1
        else:
          creat_ledger_obj["BALANCE"] = float(acct_to_update.CLOSNG_BLNCE) - float(payment_amount)
          creat_ledger_obj["ORDINAL"] = 1

        crt_acct_leg_serializer = AddAcctLedgerSerializer(data=creat_ledger_obj)
        crt_acct_leg_serializer.is_valid(raise_exception=True)
        crt_acct_leg_serializer.save()

        # For Non-User Acoount
        ern_type_last_ledger_trans = Acct_Ledger.objects.filter(ACCT_ID= ern_type_creat_ledger_obj["ACCT_ID"]).order_by("-ORDINAL").first()
        if ern_type_last_ledger_trans:
          ern_type_creat_ledger_obj["BALANCE"] = float(ern_type_last_ledger_trans.BALANCE) - float(payment_amount)
          ern_type_creat_ledger_obj["ORDINAL"] = ern_type_last_ledger_trans.ORDINAL + 1
        else:
          ern_type_creat_ledger_obj["BALANCE"] = float(ern_type_acct_to_update.CLOSNG_BLNCE) - float(payment_amount)
          ern_type_creat_ledger_obj["ORDINAL"] = 1

        crt_ern_type__leg_serializer = AddAcctLedgerSerializer(data=ern_type_creat_ledger_obj)
        crt_ern_type__leg_serializer.is_valid(raise_exception=True)
        crt_ern_type__leg_serializer.save()
 
        self.updateAcctBalnce(account=acct_to_update, updated_balance=creat_ledger_obj["BALANCE"])
        self.updateAcctBalnce(account=ern_type_acct_to_update, updated_balance=ern_type_creat_ledger_obj["BALANCE"])
    
    
    def insertEarningUpdate(self, account_id, earn_transac):
        # pass
        acct_to_update =  self.findCashAcct(acct_id=account_id)
        creat_ledger_obj =  self.getLedgerObj(transac=earn_transac , name = earn_transac.ACCT_ID.ACCT_TITLE )  
        creat_ledger_obj["ACCT_ID"] = acct_to_update.ACCT_ID
        # For Non-User Acoount      
        ern_type_acct_to_update =  self.findCashAcct(acct_id=earn_transac.EARN_TYP_ACCT.ACCT_ID)
        ern_type_creat_ledger_obj =  self.getLedgerObj(transac=earn_transac , name = earn_transac.EARN_TYP_ACCT.ACCT_TITLE)  
        ern_type_creat_ledger_obj["ACCT_ID"] = ern_type_acct_to_update.ACCT_ID

        payment_amount = earn_transac.PYMNT_AMNT
        # For Acoount
        last_ledger_trans = Acct_Ledger.objects.filter(ACCT_ID= creat_ledger_obj["ACCT_ID"]).order_by("-ORDINAL").first()
        if last_ledger_trans:
          creat_ledger_obj["BALANCE"] = float(last_ledger_trans.BALANCE) - float(payment_amount)
          creat_ledger_obj["ORDINAL"] = last_ledger_trans.ORDINAL + 1
        else:
          creat_ledger_obj["BALANCE"] = float(acct_to_update.CLOSNG_BLNCE) - float(payment_amount)
          creat_ledger_obj["ORDINAL"] = 1

        crt_acct_leg_serializer = AddAcctLedgerSerializer(last_ledger_trans , data=creat_ledger_obj)
        crt_acct_leg_serializer.is_valid(raise_exception=True)
        crt_acct_leg_serializer.save()

        # For Non-User Acoount 
        ern_type_last_ledger_trans = Acct_Ledger.objects.filter(ACCT_ID= ern_type_creat_ledger_obj["ACCT_ID"]).order_by("-ORDINAL").first()
        if ern_type_last_ledger_trans:
          ern_type_creat_ledger_obj["BALANCE"] = float(ern_type_last_ledger_trans.BALANCE) - float(payment_amount)
          ern_type_creat_ledger_obj["ORDINAL"] = ern_type_last_ledger_trans.ORDINAL + 1
        else:
          ern_type_creat_ledger_obj["BALANCE"] = float(ern_type_acct_to_update.CLOSNG_BLNCE) - float(payment_amount)
          ern_type_creat_ledger_obj["ORDINAL"] = 1

        crt_ern_type__leg_serializer = AddAcctLedgerSerializer(ern_type_last_ledger_trans ,data=ern_type_creat_ledger_obj)
        crt_ern_type__leg_serializer.is_valid(raise_exception=True)
        crt_ern_type__leg_serializer.save()
 
        self.updateAcctBalnce(account=acct_to_update, updated_balance=creat_ledger_obj["BALANCE"])
        self.updateAcctBalnce(account=ern_type_acct_to_update, updated_balance=ern_type_creat_ledger_obj["BALANCE"])

    def insertExpense(self, account_id, exp_transac):
        acct_to_update =  self.findCashAcct(acct_id=account_id)
        creat_ledger_obj =  self.getLedgerObj(transac=exp_transac , name = exp_transac.ACCT_ID.ACCT_TITLE) 
        creat_ledger_obj["ACCT_ID"] = acct_to_update.ACCT_ID
        # For Non-User Acoount      
        ern_type_acct_to_update =  self.findCashAcct(acct_id=exp_transac.EXPNS_TYP_ACCT.ACCT_ID)
        ern_type_creat_ledger_obj =  self.getLedgerObj(transac=exp_transac ,name = exp_transac.EXPNS_TYP_ACCT.ACCT_TITLE)  
        ern_type_creat_ledger_obj["ACCT_ID"] = ern_type_acct_to_update.ACCT_ID

        payment_amount = exp_transac.PYMNT_AMNT

        last_ledger_trans = Acct_Ledger.objects.filter(ACCT_ID= creat_ledger_obj["ACCT_ID"]).order_by("-ORDINAL").first()
        if last_ledger_trans:
          creat_ledger_obj["BALANCE"] = float(last_ledger_trans.BALANCE) + float(payment_amount)
          creat_ledger_obj["ORDINAL"] = last_ledger_trans.ORDINAL + 1
        else:
          creat_ledger_obj["BALANCE"] = float(acct_to_update.CLOSNG_BLNCE) + float(payment_amount)
          creat_ledger_obj["ORDINAL"] = 1

        crt_acct_leg_serializer = AddAcctLedgerSerializer(data=creat_ledger_obj)
        crt_acct_leg_serializer.is_valid(raise_exception=True)
        crt_acct_leg_serializer.save()


         # For Non-User Acoount
        ern_type_last_ledger_trans = Acct_Ledger.objects.filter(ACCT_ID= ern_type_creat_ledger_obj["ACCT_ID"]).order_by("-ORDINAL").first()
        if ern_type_last_ledger_trans:
          ern_type_creat_ledger_obj["BALANCE"] = float(ern_type_last_ledger_trans.BALANCE) - float(payment_amount)
          ern_type_creat_ledger_obj["ORDINAL"] = ern_type_last_ledger_trans.ORDINAL + 1
        else:
          ern_type_creat_ledger_obj["BALANCE"] = float(ern_type_acct_to_update.CLOSNG_BLNCE) - float(payment_amount)
          ern_type_creat_ledger_obj["ORDINAL"] = 1

        crt_ern_type__leg_serializer = AddAcctLedgerSerializer(data=ern_type_creat_ledger_obj)
        crt_ern_type__leg_serializer.is_valid(raise_exception=True)
        crt_ern_type__leg_serializer.save()

        self.updateAcctBalnce(account=acct_to_update, updated_balance=creat_ledger_obj["BALANCE"])
        self.updateAcctBalnce(account=ern_type_acct_to_update, updated_balance=ern_type_creat_ledger_obj["BALANCE"])
        # pass

    def findCashAcct(self, acct_id):
        try:
          cash_queryset = Accounts.objects.get(ACCT_ID=acct_id)
          return cash_queryset
        except Accounts.DoesNotExist:
          return None
        # pass

    def cashIn(self, account_id, earn_transac):
        # pass
        cash_acct =  self.findCashAcct(acct_id=account_id)
        new_cash_obj = self.getCashObj(transac=earn_transac)

        cash_ledger_trans = CashLedger.objects.all().order_by("-ORDINAL").first()

        payment_amount = float(earn_transac.PYMNT_AMNT)
        if cash_ledger_trans:
          new_cash_obj["BALANCE"] = float(cash_ledger_trans.BALANCE) + payment_amount
          new_cash_obj["ORDINAL"] = cash_ledger_trans.ORDINAL + 1
        else:
          new_cash_obj["BALANCE"] = payment_amount
          new_cash_obj["ORDINAL"] = 1

        crt_acct_leg_serializer = AddCashLedgerSerializer(data=new_cash_obj)
        crt_acct_leg_serializer.is_valid(raise_exception=True)
        crt_acct_leg_serializer.save()

        # self.updateAcctBalnce(account=cash_acct, updated_balance=new_cash_obj["BALANCE"])

    def cashOut(self, account_id, earn_transac):
        # pass
        cash_acct =  self.findCashAcct(acct_id=account_id)
        new_cash_obj = self.getCashObj(transac=earn_transac)

        cash_ledger_trans = CashLedger.objects.all().order_by("-ORDINAL").first()

        payment_amount = float(earn_transac.PYMNT_AMNT)
        if cash_ledger_trans:
          new_cash_obj["BALANCE"] = float(cash_ledger_trans.BALANCE) - payment_amount
          new_cash_obj["ORDINAL"] = cash_ledger_trans.ORDINAL + 1
        else:
          new_cash_obj["BALANCE"] = float(cash_acct.CLOSNG_BLNCE) - payment_amount
          new_cash_obj["ORDINAL"] = 1

        crt_acct_leg_serializer = AddCashLedgerSerializer(data=new_cash_obj)
        crt_acct_leg_serializer.is_valid(raise_exception=True)
        crt_acct_leg_serializer.save()

        # self.updateAcctBalnce(account=cash_acct, updated_balance=new_cash_obj["BALANCE"])

    def addInvntryAcctTranscToLedger(self, inventory_acct, inventory_earn):
        pass
        # match inventory_acct:
        #   # moulding - pathai
        #   case 1:
        #     return self.insertEarning(account_id=inventory_acct, earn_transac=inventory_earn)
        #   # drying - paltai
        #   case 2:
        #     return self.insertEarning(account_id=inventory_acct, earn_transac=inventory_earn)
        #   # nakasi-in - nakasi
        #   case 3:
        #     return self.insertEarning(account_id=inventory_acct, earn_transac=inventory_earn)
        #   # nakasi-out - nakasi
        #   case 4:
        #     return self.insertEarning(account_id=inventory_acct, earn_transac=inventory_earn)
        #   case default:
        #     return

    def addInventoryToLedger(self, invRecord):
        financeUtil = FinanceUtil()
        earning_transac = financeUtil.addInventoryToEarning(
            inventory=invRecord)
        if earning_transac is not None:
            # ledgerTransc = LedgerTransaction(isExpense=False)
            self.insertEarning(
                account_id=earning_transac.ACCT_ID.ACCT_ID, earn_transac=earning_transac)
            # self.addInvntryAcctTranscToLedger(inventory_acct=invRecord.TRNS_TYP_ACCT_ID.ACCT_ID, inventory_earn=earning_transac)