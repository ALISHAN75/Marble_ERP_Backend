# serializer
from decimal import Decimal
from this import d
#  utils
from inventory.utility.InventoryUtil import InventoryUtil
from accounts.LedgerTransaction import LedgerTransaction
from accounts.model.Account import Accounts
from inventory.model.ProductSizes import ProductSizes
from finance.serializer.EarningTranscSerializer import AddEarningTranscSerializer
from finance.serializer.ExpenseTransSerializer import AdddExpenseTransSerializer
from inventory.model.Orders import Order_items, Orders

# serializers imports


class DeliveryUtil():

    deliveryInv = {
        "I_DETAILS": {},
        "F_DETAILS": []
    }

    def __init__(self):
        pass

    def updateDeliveryInInventory(self, deliveryRecord, deliveryItemRecord, orderItem, request_user):
        deliverySqft = round(
            (orderItem.REQ_SQFT / orderItem.REQ_QTY) * Decimal(deliveryItemRecord.PROD_QTY), 2)

        self.deliveryInv["INVNTRY_DT"] = deliveryRecord.DLVRY_DT
        self.deliveryInv["LABOUR_SQFT"] = deliverySqft
        self.deliveryInv["TRANS_UNIT_COST"] = deliveryItemRecord.UNIT_PRICE_wDLVRY

        invDetails = self.deliveryInv["I_DETAILS"]
        invDetails["PROD_ID"] = orderItem.PRODUCT_ID.PRODUCT_ID
        invDetails["SIZE_ID"] = orderItem.DLVRY_SIZE_ID.SIZE_ID
        invDetails["IS_SIZED"] = orderItem.IS_SIZED
        invDetails["IS_SECTIONED"] = orderItem.IS_SECTIONED
        invDetails["IS_GOLA"] = orderItem.IS_GOLA
        invDetails["IS_POLISHED"] = orderItem.IS_POLISHED

        if deliveryRecord.IS_SALE == 1:
            self.deliveryInv["TRANS_TYP"] = "Sale"
            self.deliveryInv["LABOUR_COST"] = 0.00
            self.deliveryInv["ACCT_ID"] = deliveryRecord.CUST_ACCT_ID.ACCT_ID
            invDetails["QTY"] = -(deliveryItemRecord.PROD_QTY)
            invDetails["QTY_SQFT"] = -(deliverySqft)
            invDetails["TOTAL_PROD_UNIT_COST"] = 0.00
        else:
            self.deliveryInv["TRANS_TYP"] = "Purchase"
            self.deliveryInv["LABOUR_COST"] = deliveryItemRecord.DLVRY_ITEM_TOTAL
            self.deliveryInv["ACCT_ID"] = deliveryRecord.MRCHNT_ACCT_ID.ACCT_ID
            invDetails["QTY"] = deliveryItemRecord.PROD_QTY
            invDetails["QTY_SQFT"] = deliverySqft
            invDetails["TOTAL_PROD_UNIT_COST"] = deliveryItemRecord.UNIT_PRICE_wDLVRY

        self.deliveryInv["I_DETAILS"] = invDetails

        inventoryUtil = InventoryUtil()
        inventoryUtil.updateInventoryOnDelivery(
            deliveryInvRec=self.deliveryInv, req_user=request_user)

    def addDeliveryToEarning(self, purchaseDelivery):
        earning_obj = {
            "PYMNT_DT": purchaseDelivery.DLVRY_DT,
            "PYMNT_BY": purchaseDelivery.MRCHNT_ACCT_ID.ACCT_TITLE,
            "IS_CASH": 0,
            "DLVRY_ID": purchaseDelivery.DLVRY_ID,
            "PYMNT_AMNT": purchaseDelivery.DLVRY_wORDR_COST,
            "NOTES": "Delivery dispatched to" + purchaseDelivery.MRCHNT_ACCT_ID.ACCT_TITLE + "of" + str(purchaseDelivery.DLVRY_wORDR_COST),
            "ACCT_ID": purchaseDelivery.MRCHNT_ACCT_ID.ACCT_ID,
            # "EMP_ID": purchaseDelivery.DLVRY_BY_EMP_ID.EMP_ID,
            "REC_ADD_BY": purchaseDelivery.REC_MOD_BY
        }
        EARN_TYP_ACCT = Accounts.objects.get(ACCT_TITLE='Sale/Purchase')
        earning_obj["EARN_TYP_ACCT"] = EARN_TYP_ACCT.ACCT_ID

        create_serializer = AddEarningTranscSerializer(data=earning_obj)
        if create_serializer.is_valid(raise_exception=True):
            return create_serializer.save()
        return None

    def addDeliveryToExpense(self, saleDelivery):
        expense_obj = {
            "PAYMNT_DT": saleDelivery.DLVRY_DT,
            "IS_CASH": 0,
            "PYMENT_TO": saleDelivery.CUST_ACCT_ID.ACCT_TITLE,
            "DLVRY_ID": saleDelivery.DLVRY_ID,
            "PYMNT_AMNT": saleDelivery.DLVRY_wORDR_COST,
            "NOTES": saleDelivery.DLVRY_DETAIL,
            "ACCT_ID": saleDelivery.CUST_ACCT_ID.ACCT_ID,
            # "PYMNT_BY_EMP_ID": saleDelivery.DLVRY_BY_EMP_ID.EMP_ID,
            "REC_ADD_BY": saleDelivery.REC_MOD_BY,
            "TOTAL_noTAX": saleDelivery.DLVRY_wORDR_COST
        }

        EXPNS_TYP_ACCT = Accounts.objects.get(ACCT_TITLE='Sale/Purchase')
        expense_obj["EXPNS_TYP_ACCT"] = EXPNS_TYP_ACCT.ACCT_ID

        create_serializer = AdddExpenseTransSerializer(data=expense_obj)
        if create_serializer.is_valid(raise_exception=True):
            return create_serializer.save()
        return None

    def onDeliveryUpdateLedger(self, deliveryRecord):
        if deliveryRecord.IS_SALE == 1:
            expenseRecord = self.addDeliveryToExpense(
                saleDelivery=deliveryRecord)
            ledger = LedgerTransaction(isExpense=True)
            # ledger.isExpense = True
            ledger.insertExpense(
                account_id=expenseRecord.ACCT_ID.ACCT_ID, exp_transac=expenseRecord)
        else:
            earningRecord = self.addDeliveryToEarning(
                purchaseDelivery=deliveryRecord)
            ledger = LedgerTransaction(isExpense=False)
            ledger.insertEarning(
                account_id=earningRecord.ACCT_ID.ACCT_ID, earn_transac=earningRecord)

    def getProductItemVolume(self, deliveryItems, orderUtil):
        totalVolume = Decimal(0)
        productItemVolume = []
        for delivery_item in deliveryItems:
            orderItem = delivery_item["ORDR_ITEM_ID"]
            ordrItem_qs = orderUtil.findOrderItem(
                order_item_id=orderItem)
            if ordrItem_qs.IS_GEN_PROD == 1:
                qty = round(Decimal(delivery_item["PROD_QTY"]), 2)
                volume = qty
            else:
                productSize = ProductSizes.objects.get(
                    SIZE_ID=ordrItem_qs.DLVRY_SIZE_ID.SIZE_ID)
                dimensions = productSize.LENGTH * \
                    productSize.WIDTH * (productSize.THICKNESS / 8)
                qty = round(Decimal(delivery_item["PROD_QTY"]), 2)
                volume = dimensions * qty

            productItemVolume.append(volume)
            totalVolume = totalVolume + volume
        return totalVolume, productItemVolume

    def calcCostPerUnitDelQty(self, deliveryItem, deliveryCost,  productItemVolume, totalVolume):
        percentVolume = productItemVolume / totalVolume
        delCostPerSqft = round(
            Decimal(percentVolume * deliveryCost) / deliveryItem.PROD_QTY_SQFT, 2)
        deliveryItem.UNIT_DLVRY = delCostPerSqft
        deliveryItem.save()
        # deliveryItem.UNIT_PRICE_wDLVRY = PROD_TOTL_PRICE
        # deliveryItem.UNIT_PRICE_wDLVRY = UNIT_DLVRY
        return deliveryItem

    def saveUnitPriceWDelivery(self, deliveryItem, orderItem):
        deliveryItem.UNIT_PRICE_noDLVRY = round(orderItem.PROD_TOTL_PRICE, 2)
        deliveryItem.UNIT_PRICE_wDLVRY = round(
            orderItem.PROD_TOTL_PRICE + deliveryItem.UNIT_DLVRY, 2)
        deliveryItem.DLVRY_ITEM_TOTAL = round(
            (orderItem.PROD_TOTL_PRICE + deliveryItem.UNIT_DLVRY) * deliveryItem.PROD_QTY_SQFT, 2)
        deliveryItem.save()

        return deliveryItem

    def updateOrderStatus(self, orderIdToUpdate):
        queryset = Order_items.objects.filter(ORDR_ID=orderIdToUpdate, IS_DLVRD=0)
        if queryset is not None: 
            return
        order_qs = Orders.objects.get(ORDR_ID=orderIdToUpdate)
        order_qs.DELVRY_STS = 1
        order_qs.IS_ACTIVE = 0
        order_qs.save()
