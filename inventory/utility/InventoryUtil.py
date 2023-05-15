from decimal import Decimal
# models imports
from inventory.model.Products import Products
from inventory.model.ProductSizes import ProductSizes
from inventory.model.Inventory import Transaction_Details
from inventory.model.Inventory import Transaction_Details
from inventory.model.Breakage import Breakage
# serializers imports
from inventory.serializers.InventorySerializer import AddInvTransactionSerializer
from inventory.serializers.ProductsSerializer import ProductsSerializer
from inventory.serializers.ProductSizesSerializer import ProductSizesSerializer
from inventory.serializers.TransactionDetailsSerializer import AddTransactionDetailsSerializer, TransactionDetailsSerializer
from inventory.serializers.BreakageSerializer import BreakageSerializer
from accounts.model.Account import Accounts
from inventory.model.ProductSizes import ProductSizes
from finance.serializer.EarningTranscSerializer import AddEarningTranscSerializer
from inventory.model.ProductInventory import ProductInventory
from accounts.LedgerTransaction import LedgerTransaction


class InventoryUtil():

    invDict = {
        "Sectioning": "IS_SECTIONED",
        "Gola": "IS_GOLA",
        "Sizing": "IS_SIZED",
        "Polishing": "IS_POLISHED"
    }
    prevInitialRec = None
    prevFinalRec = None

    inventoryRec = None
    user = None
    finalVolume = 0

    initialAttr = None
    breakage = None
    finalAttr = None

    def __init__(self):
        pass

    def getOrCreateProduct(self, productNameID, categoryID, usageID, request_user):
        try:
            product_qs = Products.objects.get(
                PROD_NM_ID=productNameID, CAT_ID=categoryID, USAGE_ID=usageID)
            return product_qs
        except Products.DoesNotExist:
            product_to_add = {
                "CAT_ID": categoryID,
                "USAGE_ID": usageID,
                "PROD_NM_ID": productNameID,
                "REC_ADD_BY": request_user.id,
                "REC_MOD_BY": request_user.id
            }
            createSerializer = ProductsSerializer(data=product_to_add)
            createSerializer.is_valid(raise_exception=True)
            product = createSerializer.save()
            return product

    def getOrCreateSize(self, length, width, thickness, request_user):
        try:
            size_qs = ProductSizes.objects.get(
                WIDTH=width, LENGTH=length, THICKNESS=thickness)
            return size_qs
        except ProductSizes.DoesNotExist:
            size_to_add = {
                "WIDTH": width,
                "LENGTH": length,
                "THICKNESS": thickness,
                "REC_ADD_BY": request_user.id,
                "REC_MOD_BY": request_user.id
            }
            createSerializer = ProductSizesSerializer(data=size_to_add)
            createSerializer.is_valid(raise_exception=True)
            product = createSerializer.save()
            return product

    def findLastInventoryRecord(self, invToFind):
        try:
            prevInvRecordQS = Transaction_Details.objects.filter(
                PROD_ID=invToFind["PROD_ID"],
                SIZE_ID=invToFind["SIZE_ID"],
                IS_GOLA=invToFind["IS_GOLA"],
                IS_POLISHED=invToFind["IS_POLISHED"],
                IS_SECTIONED=invToFind["IS_SECTIONED"],
                IS_SIZED=invToFind["IS_SIZED"],
                # IS_AVLBL=1,
            ).last()
            # prevInvRecordQS = ProductInventory.objects.get(
            #     PROD_ID=invToFind["PROD_ID"],
            #     SIZE_ID=invToFind["SIZE_ID"],
            #     IS_GOLA=invToFind["IS_GOLA"],
            #     IS_POLISHED=invToFind["IS_POLISHED"],
            #     IS_SECTIONED=invToFind["IS_SECTIONED"],
            #     IS_SIZED=invToFind["IS_SIZED"],
            #     # IS_AVLBL=1
            # )
            return prevInvRecordQS
        except:
            return None

    def updateLastRecordStatus(self, lastInvTransaction):
        if lastInvTransaction is not None:
            lastInvTransaction.IS_LAST_REC = 0
            lastInvTransaction.save()

    def updateAvailQtyAndSqft(self, invRecToUpdate, prevInvQuerySet):
        if prevInvQuerySet is not None:
            invRecToUpdate["AVLBL_QTY"] = round(Decimal(prevInvQuerySet.AVLBL_QTY) + Decimal(invRecToUpdate["QTY"]), 2)
            invRecToUpdate["AVLBL_SQFT"] = round(Decimal(prevInvQuerySet.AVLBL_SQFT) + \
                Decimal(invRecToUpdate["QTY_SQFT"]), 2)
        else:
            invRecToUpdate["AVLBL_QTY"] = round(Decimal(invRecToUpdate["QTY"]), 2)
            invRecToUpdate["AVLBL_SQFT"] = round(Decimal(invRecToUpdate["QTY_SQFT"]), 2)

        if float(invRecToUpdate["AVLBL_QTY"]) > float(0):
            invRecToUpdate["IS_AVLBL"] = 1
        return invRecToUpdate

    def updateProductUnitCost(self, prevInvRec, invDetailRecord,  totalVolume):
        InvProdQtySqft = Decimal(invDetailRecord["QTY_SQFT"])

        percentVolume = 1.0
        if totalVolume > 0:
            percentVolume = (
                Decimal(invDetailRecord["THICKNESS"]) * InvProdQtySqft) / totalVolume

        if self.prevInitialRec is not None and Decimal(invDetailRecord["QTY"]) > Decimal(0.00):
            initialSqft = Decimal(self.initialAttr["QTY_SQFT"])
            prevInitialProdCost = Decimal(
                self.prevInitialRec.TOTAL_AVG_PROD_UNIT_COST)

            costbyTransType = {
                "Sectioning": ((((prevInitialProdCost) * (-1 * initialSqft)) + (Decimal(self.inventoryRec.TRANS_UNIT_COST) * Decimal(self.inventoryRec.LABOUR_SQFT))) / Decimal(InvProdQtySqft)) * Decimal(percentVolume),
                "Gola":   (((prevInitialProdCost * (-1 * initialSqft)) + (Decimal(self.inventoryRec.TRANS_UNIT_COST) * Decimal(self.inventoryRec.LABOUR_RUN_FT))) / Decimal(InvProdQtySqft)),
                "Sizing":   (((prevInitialProdCost * (-1 * initialSqft)) + (Decimal(self.inventoryRec.TRANS_UNIT_COST) * Decimal(self.inventoryRec.LABOUR_SQFT))) / Decimal(InvProdQtySqft)) * Decimal(percentVolume),
                "Polishing": (((prevInitialProdCost * (-1 * initialSqft)) + (Decimal(self.inventoryRec.TRANS_UNIT_COST) * Decimal(self.inventoryRec.LABOUR_SQFT))) / Decimal(InvProdQtySqft))
            }

            invDetailRecord["TOTAL_PROD_UNIT_COST"] = round(
                costbyTransType.get(self.inventoryRec.TRANS_TYP, prevInitialProdCost), 2)
            invDetailRecord["TOTAL_AVG_PROD_UNIT_COST"] = round(Decimal(
                invDetailRecord["TOTAL_PROD_UNIT_COST"]), 2)

        elif self.prevInitialRec is not None and Decimal(invDetailRecord["QTY"]) < Decimal(0.00):
            invDetailRecord["TOTAL_PROD_UNIT_COST"] = self.prevInitialRec.TOTAL_PROD_UNIT_COST
            invDetailRecord["TOTAL_AVG_PROD_UNIT_COST"] = self.prevInitialRec.TOTAL_PROD_UNIT_COST

        if prevInvRec is not None:
            prevRecAvailSqft = Decimal(prevInvRec.AVLBL_SQFT)
            prevFinalProdCost = Decimal(prevInvRec.TOTAL_AVG_PROD_UNIT_COST)
            InvRecUnitCost = Decimal(invDetailRecord["TOTAL_PROD_UNIT_COST"])

            invDetailRecord["TOTAL_AVG_PROD_UNIT_COST"] = round(
                (prevRecAvailSqft * prevFinalProdCost + InvProdQtySqft * InvRecUnitCost) / (prevRecAvailSqft + InvProdQtySqft), 2)

        return invDetailRecord

    # def updateTransCheckByType(self, invRecordQS, initialInvRecord, finalInvRecord):
    #   finalInvRecord["IS_SECTIONED"] = initialInvRecord["IS_SECTIONED"]
    #   finalInvRecord["IS_GOLA"] = initialInvRecord["IS_GOLA"]
    #   finalInvRecord["IS_SIZED"] = initialInvRecord["IS_SIZED"]
    #   finalInvRecord["IS_POLISHED"] = initialInvRecord["IS_POLISHED"]

    #   if invRecordQS.TRANS_TYP in self.invDict:
    #     dictKey = self.invDict[invRecordQS.TRANS_TYP]
    #     finalInvRecord[dictKey] = 1
    #   return finalInvRecord

    def insertInitialInventory(self):
        self.initialAttr["INV_TRANS_ID"] = self.inventoryRec.INV_TRANS_ID
        self.initialAttr["IS_AVLBL"] = 0
        self.initialAttr["REC_ADD_BY"] = self.user.id

        self.prevInitialRec = self.findLastInventoryRecord(self.initialAttr)
        self.initialAttr = self.updateProductUnitCost(
            prevInvRec=self.prevInitialRec,
            invDetailRecord=self.initialAttr,
            totalVolume=0
        )
        self.initialAttr = self.updateAvailQtyAndSqft(
            self.initialAttr,
            self.prevInitialRec
        )

        create_serializer = AddTransactionDetailsSerializer(
            data=self.initialAttr)
        create_serializer.is_valid(raise_exception=True)
        initial_inv_detail = create_serializer.save()
        self.updateLastRecordStatus(self.prevInitialRec)

        return initial_inv_detail

    def insertFinalInventory(self):
        self.finalAttr["INV_TRANS_ID"] = self.inventoryRec.INV_TRANS_ID
        self.finalAttr["IS_AVLBL"] = 0
        self.finalAttr["REC_ADD_BY"] = self.user.id

        # fInvAfterCheck = self.updateTransCheckByType(
        #   invRecordQS=inv_instance,
        #   initialInvRecord=initial_attr,
        #   finalInvRecord=final_attr
        #   )
        self.prevFinalRec = self.findLastInventoryRecord(self.finalAttr)
        self.finalAttr = self.updateProductUnitCost(
            prevInvRec=self.prevFinalRec,
            invDetailRecord=self.finalAttr,
            totalVolume=self.finalVolume
        )
        self.finalAttr = self.updateAvailQtyAndSqft(
            invRecToUpdate=self.finalAttr,
            prevInvQuerySet=self.prevFinalRec
        )

        create_serializer = AddTransactionDetailsSerializer(
            data=self.finalAttr)
        create_serializer.is_valid(raise_exception=True)
        create_serializer.save()
        self.updateLastRecordStatus(self.prevFinalRec)
 
   
    # Breakage methods starts here #
    def findProductBreakage(self):
        try:
            lastBreakagesRec = Breakage.objects.filter(
                PROD_ID=self.breakage["PROD_ID"], 
                # SIZE_ID=self.breakage["SIZE_ID"],
                # IS_SIZED=self.breakage["IS_SIZED"],
                # IS_SECTIONED=self.breakage["IS_SECTIONED"], 
                # IS_POLISHED=self.breakage["IS_POLISHED"], 
                # IS_GOLA=self.breakage["IS_GOLA"], 
            ).last()
            return lastBreakagesRec
        except:
            return None


    def getCalcProductBreakage(self):
        breakageRecord = self.findProductBreakage()

        if breakageRecord is not None:
            self.breakage["AVLBL_SQFT"] = round(Decimal(self.breakage["AVLBL_SQFT"]) + breakageRecord.AVLBL_SQFT, 2)


    def insertInventoryBreakage(self, initialProduct):
        if self.breakage["AVLBL_SQFT"] <= 0:
            return
        self.breakage["INV_TRANS_ID"] = self.inventoryRec.INV_TRANS_ID
        self.breakage["PROD_ID"] =  initialProduct.PROD_ID.PRODUCT_ID 
        # self.breakage["SIZE_ID"] =  initialProduct.SIZE_ID.SIZE_ID 
        # self.breakage["IS_SIZED"] =  initialProduct.IS_SIZED 
        # self.breakage["IS_SECTIONED"] =  initialProduct.IS_SECTIONED
        # self.breakage["IS_POLISHED"] =  initialProduct.IS_POLISHED
        # self.breakage["IS_GOLA"] =  initialProduct.IS_GOLA 
        self.breakage["REC_ADD_BY"] = self.user.id
        self.getCalcProductBreakage()
        create_serializer = BreakageSerializer(
            data=self.breakage)
        create_serializer.is_valid(raise_exception=True)
        create_serializer.save()
    # Breakage methods starts here #


    def deleteInitialInventory(self):
        self.initialAttr["QTY"] = Decimal(-1.00) * \
            Decimal(self.initialAttr["QTY"])
        self.initialAttr["QTY_SQFT"] = Decimal(-1.00) * \
            Decimal(self.initialAttr["QTY_SQFT"])

        self.insertInitialInventory()

    def deleteFinalInventory(self):
        self.finalAttr["INV_TRANS_ID"] = self.inventoryRec.INV_TRANS_ID
        self.finalAttr["QTY"] = Decimal(-1.00) * Decimal(self.finalAttr["QTY"])
        self.finalAttr["QTY_SQFT"] = Decimal(-1.00) * \
            Decimal(self.finalAttr["QTY_SQFT"])

        self.insertFinalInventory()

    def calcAvgCostByWeightAvg(self, prevInvRec, invDetailsRec):
        productCost = Decimal(invDetailsRec["TOTAL_PROD_UNIT_COST"])
        productSqft = Decimal(invDetailsRec["QTY_SQFT"])

        if prevInvRec is not None:
            invDetailsRec["TOTAL_AVG_PROD_UNIT_COST"] = round(Decimal(
                (prevInvRec.AVLBL_SQFT * prevInvRec.TOTAL_AVG_PROD_UNIT_COST + productCost * productSqft) / (prevInvRec.AVLBL_SQFT + productSqft)), 2)
        else:
            invDetailsRec["TOTAL_AVG_PROD_UNIT_COST"] = round(productCost, 2)

        return invDetailsRec

    # inventory delivery
    def insertDeliveryInventory(self):
        self.initialAttr["INV_TRANS_ID"] = self.inventoryRec.INV_TRANS_ID
        self.initialAttr["IS_AVLBL"] = 0
        self.initialAttr["REC_ADD_BY"] = self.user.id

        self.prevInitialRec = self.findLastInventoryRecord(self.initialAttr)
        self.initialAttr = self.calcAvgCostByWeightAvg(
            prevInvRec=self.prevInitialRec, invDetailsRec=self.initialAttr)
        self.initialAttr = self.updateAvailQtyAndSqft(
            self.initialAttr,
            self.prevInitialRec
        )
        create_serializer = AddTransactionDetailsSerializer(
            data=self.initialAttr)
        create_serializer.is_valid(raise_exception=True)
        initial_inv_detail = create_serializer.save()
        self.updateLastRecordStatus(self.prevInitialRec)

        return initial_inv_detail

    def updateInventoryOnDelivery(self, deliveryInvRec, req_user):
        deliveryInvRec["REC_ADD_BY"] = req_user.id
        create_serializer = AddInvTransactionSerializer(data=deliveryInvRec)
        inventoryUtil = InventoryUtil()
        if create_serializer.is_valid():
            new_inventory = create_serializer.save()
            # invRecord
            inventoryUtil.inventoryRec = new_inventory
            # initialAttr
            inventoryUtil.initialAttr = deliveryInvRec["I_DETAILS"]
            inventoryUtil.user = req_user
            inventoryUtil.insertDeliveryInventory()
        else:
            print(create_serializer.errors)


    def addInventoryToEarning(self, inventoryRecord):
            earning_obj = {
                "PYMNT_DT": inventoryRecord.INVNTRY_DT,
                "PYMNT_BY": "Factory Owner",
                "IS_CASH": 0,
                "INVNTRY_TRANS_ID":  inventoryRecord.INV_TRANS_ID,
                "PYMNT_AMNT": inventoryRecord.LABOUR_COST,
                "NOTES": "Delivery dispatched to" + inventoryRecord.ACCT_ID.ACCT_TITLE + "of" + str(inventoryRecord.LABOUR_COST),
                "NOTES": f"{inventoryRecord.LABOUR_SQFT} Sqft Work of cost {inventoryRecord.LABOUR_COST} by Labour {inventoryRecord.ACCT_ID.ACCT_TITLE}."
                "Delivery dispatched to" + inventoryRecord.ACCT_ID.ACCT_TITLE + "of" + str(inventoryRecord.LABOUR_COST),
                "ACCT_ID": inventoryRecord.ACCT_ID.ACCT_ID,
                # "EMP_ID": purchaseDelivery.DLVRY_BY_EMP_ID.EMP_ID,
                "REC_ADD_BY": inventoryRecord.REC_ADD_BY
            }
            EARN_TYP_ACCT = Accounts.objects.get(ACCT_TITLE='Labour Expense')
            earning_obj["EARN_TYP_ACCT"] = EARN_TYP_ACCT.ACCT_ID

            create_serializer = AddEarningTranscSerializer(data=earning_obj)
            if create_serializer.is_valid(raise_exception=True):
                return create_serializer.save()
            return None
   

    def onInventoryUpdateLedger(self, inventory_transaction):
        earningRecord = self.addInventoryToEarning(inventoryRecord=inventory_transaction)
        ledger = LedgerTransaction(isExpense=False)
        ledger.insertEarning(
            account_id=earningRecord.ACCT_ID.ACCT_ID, earn_transac=earningRecord)
    

    def checkProductExistance(self, latestProduct):
        try:
            product = ProductInventory.objects.get(
                    PROD_ID=latestProduct["PROD_ID"],
                    SIZE_ID=latestProduct["SIZE_ID"],
                    IS_SIZED=latestProduct["IS_SIZED"],
                    IS_SECTIONED=latestProduct["IS_SECTIONED"],
                    IS_POLISHED=latestProduct["IS_POLISHED"],
                    IS_GOLA=latestProduct["IS_GOLA"]
                    )
            return product
        except ProductInventory.DoesNotExist:
            return None


    def checkQtyLimitExceed(self, latestProduct, existingProduct):
        if Decimal(round(abs(latestProduct["QTY"]), 2)) > existingProduct.AVLBL_QTY:
            return True
        return False