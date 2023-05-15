from django.db.models import Q
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from accounts.CustomPermission import IsUserAllowed
from accounts.renderers import UserRenderer
# util
from inventory.utility.PAY_REQ_SIZE import pay_Size, PRODUCT
# models imports
from inventory.model.Orders import Orders, Order_items
from inventory.model.ProductSizes import ProductSizes
# serializers imports
from inventory.serializers.ProductSizesSerializer import ProductSizesSerializer
from inventory.serializers.OrdersSerializer import OrderSerializer, MerchantOrderSerializer, AddOrderSerializer
from inventory.serializers.OrderItemsSerializer import OrderItemsSerializer, AddOrderItemsSerializer


class SaleProductListView(
    APIView,  # Basic View class provided by the Django Rest Framework
    UpdateModelMixin,  # Mixin that allows the basic APIView to handle PUT HTTP requests
    # Mixin that allows the basic APIView to handle DELETE HTTP request):
    DestroyModelMixin,
):
    permission_classes = [IsUserAllowed({'POST': 'inventory.add_orders', 'PUT': 'inventory.change_orders',
                                        'DELETE': 'inventory.delete_orders', 'GET': 'inventory.view_orders'})]
    renderer_classes = [UserRenderer]
    rec_is_active = 1

    def get(self, request, IS_SALE=None):

        if id:
            try:
                queryset = Orders.objects.get(ORDR_ID=id, IS_SALE=IS_SALE)
            except Orders.DoesNotExist:
                return Response({'error': 'The Sale Order does not exist.' , "error_ur" : "سیل آرڈر موجود نہیں ہے۔"}, status=400)
            read_serializer = OrderSerializer(queryset)
        else:
            if request.query_params:
                params = request.query_params
                queryset = Orders.objects.filter(Q(ORDR_DT__icontains=params['search']) | Q(ORDR_TOTAL_wTAX__icontains=params['search']) | Q(
                    ORDR_TOTAL_no_TAX__icontains=params['search']), IS_SALE=IS_SALE, IS_ACTIVE=1)
            else:
                queryset = Orders.objects.filter(IS_SALE=IS_SALE, IS_ACTIVE=1)
            read_serializer = OrderSerializer(queryset, many=True)
        return Response(read_serializer.data, status=200)

    def post(self, request, IS_SALE=None):
        #  append security fields
        request.data["REC_ADD_BY"] = request.user.id
        request.data["REC_MOD_BY"] = request.user.id
        request.data["IS_SALE"] = IS_SALE
        Dict_ORDER_ITEMS = request.data["ORDER_ITEMS"]
        create_serializer = AddOrderSerializer(data=request.data)
        if create_serializer.is_valid():
            new_sale = create_serializer.save()

            if len(Dict_ORDER_ITEMS) > 0:
                for ORDER_ITEM in Dict_ORDER_ITEMS:
                    ORDER_ITEM["ORDR_ID"] = new_sale.ORDR_ID
                    ORDER_ITEM["REC_ADD_BY"] = request.user.id
                    ORDER_ITEM["REC_MOD_BY"] = request.user.id
                    #  PAY_SIZE_ID
                    ORDER_ITEM["PAY_SIZE_ID"] = pay_Size(
                        THICKNESS=ORDER_ITEM["PAY_THICKNESS"], WIDTH=ORDER_ITEM["PAY_WIDTH"], LENGHT=ORDER_ITEM["PAY_LENGTH"], ID=request.user.id)
                    #   REQ_SIZE_ID
                    ORDER_ITEM["DLVRY_SIZE_ID"] = pay_Size(
                        THICKNESS=ORDER_ITEM["REQ_THICKNESS"], WIDTH=ORDER_ITEM["REQ_WIDTH"], LENGHT=ORDER_ITEM["REQ_LENGTH"], ID=request.user.id)
                    #   PRODUCT_ID
                    ORDER_ITEM["PRODUCT_ID"] = PRODUCT(
                        CAT_NAME=ORDER_ITEM["PROD_CAT"], PPRO_NAME=ORDER_ITEM["PROD_NAME"], PRO_USAGE=ORDER_ITEM["PROD_USAGE"], ID=request.user.id)
                    # Saving the ORDER_ITEM
                    create_item_serializer = AddOrderItemsSerializer(
                        data=ORDER_ITEM)
                    if create_item_serializer.is_valid():
                        create_item_serializer.save()
                    else:
                        return Response(create_item_serializer.errors, status=400)
                        # return Response(create_serializer.data, status=201)
            # read_serializer = OrderSerializer(new_sale)
            # return Response(read_serializer.data, status=201)
            return Response({'success' : "Data is saved successfully" ,  'success_ur' : "ڈیٹا کامیابی سے محفوظ ہو گیا ہے۔" } , status=201)
        return Response(create_serializer.errors, status=400)

    def put(self, request, id=None, IS_SALE=None):
        try:
            order_to_update = Orders.objects.get(ORDR_ID=id, IS_SALE=IS_SALE)
        except Orders.DoesNotExist:
            return Response({'error': 'The Sale Order does not exist.' , "error_ur" : "سیل آرڈر موجود نہیں ہے۔"}, status=400)
        request.data["IS_SALE"] = IS_SALE
        request.data["REC_ADD_BY"] = order_to_update.REC_ADD_BY
        request.data["REC_MOD_BY"] = request.user.id
        Dict_ORDER_ITEMS = request.data["ORDER_ITEMS"]
        # create_order_serializer = OrderSerializer(order_to_update, data=request.data)
        create_order_serializer = AddOrderSerializer(
            order_to_update, data=request.data)
        if create_order_serializer.is_valid():
            updated_purchase = create_order_serializer.save()

            for order_item in Dict_ORDER_ITEMS:
                order_item["ORDR_ID"] = order_to_update.ORDR_ID
                order_item["REC_MOD_BY"] = request.user.id
                order_item_id = "ORDR_ITEM_ID"

                # UPDATING THE EXISTING ORDDER ITEMS
                if order_item_id in order_item:
                    #  PAY_SIZE_ID
                    order_item["PAY_SIZE_ID"] = pay_Size(
                        THICKNESS=order_item["PAY_THICKNESS"], WIDTH=order_item["PAY_WIDTH"], LENGHT=order_item["PAY_LENGTH"], ID=request.user.id)
                    #  REQ_SIZE_ID
                    order_item["DLVRY_SIZE_ID"] = pay_Size(
                        THICKNESS=order_item["REQ_THICKNESS"], WIDTH=order_item["REQ_WIDTH"], LENGHT=order_item["REQ_LENGTH"], ID=request.user.id)
                    #  PRODUCT_ID
                    order_item["PRODUCT_ID"] = PRODUCT(
                        CAT_NAME=order_item["PROD_CAT"], PPRO_NAME=order_item["PROD_NAME"], PRO_USAGE=order_item["PROD_USAGE"], ID=request.user.id)
                    # Saving the ORDER_ITEM
                    order_Item_to_update = Order_items.objects.get(
                        ORDR_ITEM_ID=order_item["ORDR_ITEM_ID"], ORDR_ID=order_item["ORDR_ID"])
                    order_item["REC_ADD_BY"] = order_Item_to_update.REC_ADD_BY
                    update_ordrItem_serializer = AddOrderItemsSerializer(
                        order_Item_to_update, data=order_item)
                    # update_ordrItem_serializer = OrderItemsSerializer(order_Item_to_update, data=order_item)
                    if update_ordrItem_serializer.is_valid():
                        update_ordrItem_serializer.save()
                    else:
                        return Response(create_item_serializer.errors, status=400)
                else:
                    # ADD NEW ORDDER ITEMS
                    #  PAY_SIZE_ID
                    order_item["PAY_SIZE_ID"] = pay_Size(
                        THICKNESS=order_item["PAY_THICKNESS"], WIDTH=order_item["PAY_WIDTH"], LENGHT=order_item["PAY_LENGTH"], ID=request.user.id)
                    #  REQ_SIZE_ID
                    order_item["DLVRY_SIZE_ID"] = pay_Size(
                        THICKNESS=order_item["REQ_THICKNESS"], WIDTH=order_item["REQ_WIDTH"], LENGHT=order_item["REQ_LENGTH"], ID=request.user.id)
                    #  PRODUCT_ID
                    order_item["PRODUCT_ID"] = PRODUCT(
                        CAT_NAME=order_item["PROD_CAT"], PPRO_NAME=order_item["PROD_NAME"], PRO_USAGE=order_item["PROD_USAGE"], ID=request.user.id)
                    # Saving the ORDER_ITEM
                    order_item["REC_ADD_BY"] = request.user.id
                    create_item_serializer = AddOrderItemsSerializer(
                        data=order_item)
                    # create_item_serializer = OrderItemsSerializer(data=order_item)

                    if create_item_serializer.is_valid():
                        create_item_serializer.save()
                    else:
                        return Response(create_item_serializer.errors, status=400)
            # read_serializer = OrderSerializer(updated_purchase)
            # return Response(read_serializer.data, status=201)
            return Response({'success' : "Data is saved successfully" ,  'success_ur' : "ڈیٹا کامیابی سے محفوظ ہو گیا ہے۔" } , status=201)
        return Response(create_order_serializer.errors, status=400)

    def delete(self, request, id=None, IS_SALE=None):
        try:
            order_to_delete = Orders.objects.get(ORDR_ID=id, IS_SALE=IS_SALE)
        except Orders.DoesNotExist:
            return Response({'error': 'The Sale Order does not exist.' , "error_ur" : "سیل آرڈر موجود نہیں ہے۔"  }, status=400)

        try:
            order_items_to_delete = Order_items.objects.get(ORDR_ID=id)
        except Orders.DoesNotExist:
            return Response({'error': 'This Sale Orders item does not exist.' , "error_ur" : "یہ سیل آرڈرز آئٹم موجود نہیں ہے۔" }, status=400)

        if order_items_to_delete.DLVRD_QTY > 0:
            return Response({'error': 'Partially or fully delivered orders cannot be changed/deleted.'  , "error_ur" : "جزوی طور پر یا مکمل طور پر ڈیلیور کردہ آرڈرز کو تبدیل/حذف نہیں کیا جا سکتا۔"}, status=400)

        order_to_delete.REC_MOD_BY = request.user.id
        order_to_delete.IS_ACTIVE = 0
        order_to_delete.save()

        return Response(None, status=204)


class CustomerSaleProductListView(
    APIView,  # Basic View class provided by the Django Rest Framework
    UpdateModelMixin,  # Mixin that allows the basic APIView to handle PUT HTTP requests
    # Mixin that allows the basic APIView to handle DELETE HTTP request):
    DestroyModelMixin,
):


    renderer_classes = [UserRenderer]

    def get(self, request, id=None):
        # customer_id
        if id:
            try:
                queryset = Orders.objects.filter(
                    CUST_ACCT_ID=id, IS_ACTIVE=1, IS_SALE=1)
            except Orders.DoesNotExist:
                return Response({'error': 'The Sale Order does not exist.' , "error_ur" : "سیل آرڈر موجود نہیں ہے۔"}, status=400)
        read_serializer = MerchantOrderSerializer(queryset, many=True)
        order_item_qs = Order_items.objects.filter(ORDR_ITEM_ID=0)
        for qs in queryset:
            order_item_qs = order_item_qs | qs.ORDER_ITEMS

        order_item_serializer = OrderItemsSerializer(order_item_qs, many=True)
        return Response(order_item_serializer.data, status=200)
