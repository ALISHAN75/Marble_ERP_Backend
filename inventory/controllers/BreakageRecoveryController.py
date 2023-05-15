
from decimal import Decimal
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from accounts.CustomPermission import IsUserAllowed
from rest_framework import status
from rest_framework.permissions import AllowAny
from accounts.LedgerTransaction import LedgerTransaction
from accounts.renderers import UserRenderer
import datetime
from inventory.serializers.BreakRecoverySerializer import InvDetailsRecoverySerializer, InvRecoverySerializer
# util
from inventory.utility.InventoryUtil import InventoryUtil
# models imports
from inventory.model.Inventory import Inventory_Transactions, Transaction_Details
# serializers imports
from inventory.serializers.InventorySerializer import DelInventorySerializer, DetailedInventorySerializer, AddInvTransactionSerializer
from inventory.serializers.TransactionDetailsSerializer import TransactionDetailsSerializer, AddTransactionDetailsSerializer


class BreakageRecoveryListView(
    APIView,
    UpdateModelMixin,
    DestroyModelMixin,
):
    #   permission_classes = [IsUserAllowed({'POST': 'inventory.add_products', 'PUT': 'inventory.change_products', 'DELETE': 'inventory.delete_products', 'GET': 'inventory.view_products'})]
    permission_classes = [AllowAny]
    renderer_classes = [UserRenderer]

    def post(self, request):
        request.data["REC_ADD_BY"] = request.user.id

        create_serializer = InvRecoverySerializer(data=request.data)
        inventoryUtil = InventoryUtil()
        if create_serializer.is_valid():
            new_inventory = create_serializer.save()

            inventoryUtil.inventoryRec = new_inventory
            inventoryUtil.user = request.user

            InvDetailRecovery = request.data["INV_DETAILS"]
            InvDetailRecovery["INV_TRANS_ID"] = new_inventory.INV_TRANS_ID
            InvDetailRecovery["REC_ADD_BY"] = request.user.id
            product = inventoryUtil.getOrCreateProduct(productNameID=InvDetailRecovery["NAME_ID"], categoryID=InvDetailRecovery["CAT_ID"],
                                                       usageID=InvDetailRecovery["USAGE_ID"], request_user=request.user)
            size = inventoryUtil.getOrCreateSize(length=InvDetailRecovery["LENGTH"],
                                                 width=InvDetailRecovery["WIDTH"],
                                                 thickness=InvDetailRecovery["THICKNESS"], request_user=request.user)
            InvDetailRecovery["PROD_ID"] = product.PRODUCT_ID
            InvDetailRecovery["SIZE_ID"] = size.SIZE_ID

            inventoryUtil.initialAttr = InvDetailRecovery
            inventoryUtil.prevInitialRec = inventoryUtil.findLastInventoryRecord(
                inventoryUtil.initialAttr)
            inventoryUtil.calcAvgCostByWeightAvg(
                inventoryUtil.prevInitialRec, inventoryUtil.initialAttr)
            inventoryUtil.initialAttr = inventoryUtil.updateAvailQtyAndSqft(
                inventoryUtil.initialAttr,
                inventoryUtil.prevInitialRec
            )

            create_serializer = AddTransactionDetailsSerializer(
                data=inventoryUtil.initialAttr)
            create_serializer.is_valid(raise_exception=True)
            adjust_inv_detail = create_serializer.save()
            inventoryUtil.updateLastRecordStatus(inventoryUtil.prevInitialRec)

            # if not new_inventory.TRANS_TYP == "Adjustment":
            #     ledgerTransc = LedgerTransaction(isExpense=False)
            #     ledgerTransc.addInventoryToLedger(invRecord=new_inventory)

            # read_serializer = TransactionDetailsSerializer(adjust_inv_detail)
            return Response({'success': f'{new_inventory.TRANS_TYP} is  made Successfully.' , 'success_ur': f'کامیابی سے کی گئی ہے۔ {new_inventory.TRANS_TYP}'   }, status=status.HTTP_201_CREATED)
        return Response(create_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # def delete(self, request, id=None):
    #     try:
    #         inv_to_delete = Inventory_Transactions.objects.get(INV_TRANS_ID=id)
    #     except Inventory_Transactions.DoesNotExist:
    #         return Response({'error': 'This Inventory Transaction item does not exist.' , 'error_ur': 'یہ انوینٹری ٹرانزیکشن آئٹم موجود نہیں ہے۔'  }, status=400)
    #     inv_serializer = DelInventorySerializer(inv_to_delete)
    #     updated_serializer = inv_serializer.data
    #     updated_serializer['LABOUR_COST'] = Decimal(
    #         -1.00) * Decimal(inv_serializer.data['LABOUR_COST'])
    #     updated_serializer['LABOUR_SQFT'] = Decimal(
    #         -1.00) * Decimal(inv_serializer.data['LABOUR_SQFT'])
    #     updated_serializer["LABOUR_RUN_FT"] = Decimal(
    #         -1.00) * Decimal(inv_serializer.data["LABOUR_RUN_FT"])

    #     create_serializer = DelInventorySerializer(data=updated_serializer)
    #     create_serializer.is_valid(raise_exception=True)
    #     deleted_inv = create_serializer.save()

    #     total_volume = 0
    #     inventoryUtil = InventoryUtil()
    #     inventoryUtil.inventoryRec = deleted_inv
    #     inventoryUtil.user = request.user

    #     # inventoryUtil.initialAttr = request.data["I_DETAILS"]
    #     # for InvDetails in request.data["TRANSC_DETALS"]:
    #     # for index, InvDetails in enumerate(request.data["TRANSC_DETALS"]):
    #     #   if index > 0:
    #     #     total_volume += Decimal(InvDetails["THICKNESS"]) * Decimal(InvDetails["QTY_SQFT"])
    #     # inventoryUtil.finalVolume = total_volume

    #     for invDetail in inv_serializer.data["TRANSC_DETALS"]:
    #         inventoryUtil.initialAttr = invDetail
    #         inventoryUtil.deleteInitialInventory()

    #     ledgerTransc = LedgerTransaction(isExpense=False)
    #     ledgerTransc.addInventoryToLedger(invRecord=deleted_inv)

    #     # read_serializer = DetailedInventorySerializer(deleted_inv)
    #     # inv_details_qs = Transaction_Details.objects.filter(INV_TRANS_ID=inv_to_delete.INV_TRANS_ID)

    #     # inventory_to_delete.REC_MOD_BY = request.user.id
    #     # inventory_to_delete.IS_ACTIVE = 0
    #     # inventory_to_delete.save()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
