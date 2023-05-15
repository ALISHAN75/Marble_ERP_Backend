from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from accounts.renderers import UserRenderer
from decimal import Decimal
from django.contrib.auth.models import Group
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
# models
from inventory.serializers.TransactionDetailsSerializer import AddInvAdjustmentSerializer, TransactionDetailsSerializer, AddTransactionDetailsSerializer
from inventory.utility.InventoryUtil import InventoryUtil
from inventory.model.ProductInventory import ProductInventory
from inventory.model.Products import Products
# serializers


class InventoryAdjustmentView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        request.data["REC_ADD_BY"] = request.user.id
        request.data["REC_MOD_BY"] = request.user.id

        craete_serializer = AddInvAdjustmentSerializer(data=request.data)
        craete_serializer.is_valid(raise_exception=True)
        inventoryUtil = InventoryUtil()
        inventoryUtil.initialAttr = request.data
        inventoryUtil.initialAttr["IS_AVLBL"] = 0

        product = inventoryUtil.getOrCreateProduct(
            productNameID=request.data["NAME_ID"],
            categoryID=request.data["CAT_ID"],
            usageID=request.data["USAGE_ID"],
            request_user=request.user
        )
        size = inventoryUtil.getOrCreateSize(
            length=request.data["LENGTH"],
            width=request.data["WIDTH"],
            thickness=request.data["THICKNESS"],
            request_user=request.user
        )

        inventoryUtil.initialAttr["PROD_ID"] = product.PRODUCT_ID
        inventoryUtil.initialAttr["SIZE_ID"] = size.SIZE_ID

        inventoryUtil.prevInitialRec = inventoryUtil.findLastInventoryRecord(
            inventoryUtil.initialAttr)
        inventoryUtil.calcAvgCostByWeightAvg(
            inventoryUtil.prevInitialRec, inventoryUtil.initialAttr)
        inventoryUtil.initialAttr = inventoryUtil.updateAvailQtyAndSqft(
            inventoryUtil.initialAttr,
            inventoryUtil.prevInitialRec
        )
        
        if float(inventoryUtil.initialAttr["QTY"]) < 0:
            productFound = inventoryUtil.checkProductExistance(latestProduct=inventoryUtil.initialAttr)
            if productFound is None:
                return Response({"error" : "Product does not exist in Inventory" ,  "error_ur" : "پروڈکٹ انوینٹری میں موجود نہیں ہے" }, status=status.HTTP_400_BAD_REQUEST)
            if inventoryUtil.checkQtyLimitExceed(latestProduct=inventoryUtil.initialAttr, existingProduct=productFound):
                return Response({"error" : "Quantity must be less than or equal to stock" ,  "error_ur" : "مقدار اسٹاک سے کم یا اس کے برابر ہونی چاہیے"}, status=status.HTTP_400_BAD_REQUEST)

        create_serializer = AddTransactionDetailsSerializer(
            data=inventoryUtil.initialAttr)
        create_serializer.is_valid(raise_exception=True)
        adjust_inv_detail = create_serializer.save()
        inventoryUtil.updateLastRecordStatus(inventoryUtil.prevInitialRec)

        # adjustment_inv = craete_serializer.save()

        # read_serializer = TransactionDetailsSerializer(adjust_inv_detail)
        return Response({'success': 'Adjustment made Successfully.'  , 'success_ur': 'ایڈجسٹمنٹ کامیابی سے کی گئی۔'}, status=status.HTTP_201_CREATED)
    

    # def checkProductExistance(self, latestProduct):
    #     try:
    #         product = ProductInventory.objects.get(
    #                 PROD_ID=latestProduct["PROD_ID"],
    #                 SIZE_ID=latestProduct["SIZE_ID"],
    #                 IS_SIZED=latestProduct["IS_SIZED"],
    #                 IS_SECTIONED=latestProduct["IS_SECTIONED"],
    #                 IS_POLISHED=latestProduct["IS_POLISHED"],
    #                 IS_GOLA=latestProduct["IS_GOLA"]
    #                 )
    #         return product
    #     except ProductInventory.DoesNotExist:
    #         return None


    # def checkQtyLimitExceed(self, latestProduct, existingProduct):
    #     if Decimal(round(abs(latestProduct["QTY"]), 2)) > existingProduct.AVLBL_QTY:
    #         return True
    #     return False
