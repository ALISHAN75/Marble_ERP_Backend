# serializers imports
from finance.serializer.EarningTranscSerializer import EarningTranscSerializer


class FinanceUtil():

    def __init__(self):
        pass

    def createInventoryEarning(self, invRecord):
        return {
            "PYMNT_DT": invRecord.INVNTRY_DT,
            "PYMNT_AMNT": invRecord.LABOUR_COST,
            "ACCT_ID": invRecord.ACCT_ID.ACCT_ID,
            # "ACCT_ID": inventory.ACCT_ID.ACCT_ID,
            "INVNTRY_TRANS_ID":  invRecord.INV_TRANS_ID,
            # "EMP_ID": 1,
            "NOTES": f"{invRecord.LABOUR_SQFT} Sqft Work of cost {invRecord.LABOUR_COST} by Labour {invRecord.ACCT_ID.ACCT_ID}-{invRecord.ACCT_ID.ACCT_TITLE}.",
            "REC_ADD_BY": invRecord.REC_ADD_BY
        }

    def addInventoryToEarning(self, inventory):
        earningRec = self.createInventoryEarning(invRecord=inventory)

        create_serializer = EarningTranscSerializer(data=earningRec)
        if create_serializer.is_valid(raise_exception=True):
            return create_serializer.save()
        return None
