from django.db.models import Q
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from accounts.CustomPermission import IsUserAllowed
from rest_framework import status
from accounts.renderers import UserRenderer
# util
import json
from decimal import Decimal
import math
from datetime import datetime
import pandas as pd
from django.db import connection
from inventory.utility.PAY_REQ_SIZE import pay_Size, PRODUCT
from inventory.utility.DataConversion import dateConversion
# models imports
from inventory.model.Quotations import Quotations
from inventory.model.Orders import Orders, Order_items
from inventory.model.ProductSizes import ProductSizes
from accounts.model.Account import Accounts
from finance.model.Earning_Transactions import Earning_Transactions 
# serializers imports
from inventory.serializers.ProductSizesSerializer import ProductSizesSerializer
from inventory.serializers.OrdersSerializer import OrderSerializer, MerchantOrderSerializer, AddOrderSerializer
from inventory.serializers.OrderItemsSerializer import OrderItemsSerializer, AddOrderItemsSerializer , AddGeneralOrderItemsSerializer
from accounts.LedgerTransaction import LedgerTransaction
from finance.serializer.EarningTranscSerializer import AddEarningTranscSerializer

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

             
    def getOne(self, request, id):
        if id:
            try:
                query = """ CALL `datafunc_Mabrle_ERP_wUrdu`.`ORDR_List`("""+str(id)+""", 1, "", 1, 1000000); """     
                orders = pd.read_sql(query, connection)
                query = """CALL `datafunc_Mabrle_ERP_wUrdu`.`ORDR_Detail`( 1 , """+str(id)+""");  """    
                orders_items_data = pd.read_sql(query, connection)
            except ConnectionError:
                return Response({"error" : "Database Connection Error" , "error_ur" :  "ڈیٹا بیس کنکشن کی خرابی " } , status=status.HTTP_400_BAD_REQUEST)
   

        if orders.empty:
            return Response({"error" : "No record found" , "error_ur" : "کوئی ریکارڈ نہیں ملا" }, status=status.HTTP_400_BAD_REQUEST)
        else:
            orders = orders.fillna('')
            orders_items_data = orders_items_data.fillna('')
            orders_data=orders.to_dict(orient='records')[0]
            orders_data['ORDR_ITEMS'] = orders_items_data.to_dict(orient='records')
            return Response(orders_data  , status=status.HTTP_200_OK)

             

    def getAll(self):
        try:
            query = """ CALL `datafunc_Mabrle_ERP_wUrdu`.`ORDR_List`(0, 1, "", 1, 1000000); """    
            my_data = pd.read_sql(query, connection)
        except ConnectionError:
            return Response({"error" : "Database Connection Error" , "error_ur" :  "ڈیٹا بیس کنکشن کی خرابی " }, status=status.HTTP_400_BAD_REQUEST)

        if my_data.empty:
            return Response({"error" : "No record found" , "error_ur" : "کوئی ریکارڈ نہیں ملا" }, status=status.HTTP_400_BAD_REQUEST)
        else:
            my_data = my_data.fillna('')
            return Response(my_data.to_dict(orient='records'), status=status.HTTP_200_OK)

    def searchActive(self, params):
        page = int(params.get('page' , 1) ) 
        parPage = params.get('perPage' , 10)
        q = params.get('q' , '') 
        q = dateConversion(q)
        try:
            query = """ CALL `datafunc_Mabrle_ERP_wUrdu`.`ORDR_List`(0, 1, '"""+q+"""', """+str(page)+""", """+str(parPage)+"""); """       
            my_data = pd.read_sql(query, connection)
            query = """ select FOUND_ROWS() """       
            total = pd.read_sql(query, connection)

        except ConnectionError:
                return Response({"error" : "Database Connection Error" , "error_ur" :  "ڈیٹا بیس کنکشن کی خرابی " }, status=status.HTTP_400_BAD_REQUEST)  
        
        if my_data.empty:
            return Response([], status=status.HTTP_200_OK)
        else:
            total = total.iloc[0,0]
            my_data = my_data.fillna('')
            return Response({'data' :my_data.to_dict(orient='records'), 'total' : total , 'Page' : page , 'last_Page' : math.ceil( total / int(parPage) )  }, status=status.HTTP_200_OK , )        
        
    def get(self, request, id=None):
        if id:
            return self.getOne(request, id)
        elif request.query_params:
            return self.searchActive(params=request.query_params)
        else:
            return self.getAll()


    def post(self, request):
        #  append security fields
        request.data["REC_ADD_BY"] = request.user.id
        request.data["REC_MOD_BY"] = request.user.id
        request.data["IS_SALE"] = 1
        ADV_PAYMENT = {}
        try:
            Dict_ORDER_ITEMS = request.data["ORDER_ITEMS"]
        except:
            pass
        if "QUOTE_ID" in request.data:
            try:
                quot_to_update =Quotations.objects.get(QUOTE_ID= request.data["QUOTE_ID"])
            except Orders.DoesNotExist:
                return Response({'error': 'The Sale Order does not exist.' ,  "error_ur" : "سیل آرڈر موجود نہیں ہے۔"}, status=400)
            quot_to_update.REC_MOD_BY = request.user.id
            quot_to_update.IS_NOW_ORDER = 1
            quot_to_update.save()

        create_serializer = AddOrderSerializer(data=request.data)
        if create_serializer.is_valid():
            new_sale = create_serializer.save()
            if len(Dict_ORDER_ITEMS) > 0:
                for ORDER_ITEM in Dict_ORDER_ITEMS:
                    ORDER_ITEM["ORDR_ID"] = new_sale.ORDR_ID
                    ORDER_ITEM["REC_ADD_BY"] = request.user.id
                    ORDER_ITEM["REC_MOD_BY"] = request.user.id
                    if ORDER_ITEM["IS_GEN_PROD"] ==1:
                        create_item_serializer = AddGeneralOrderItemsSerializer(data=ORDER_ITEM)
                        if create_item_serializer.is_valid():
                            create_item_serializer.save()
                        else:
                            return Response(create_item_serializer.errors, status=400)
                    else:
                        #  PAY_SIZE_ID
                        if "PAY_THICKNESS" in ORDER_ITEM and "PAY_WIDTH" in ORDER_ITEM  and "PAY_LENGTH" in ORDER_ITEM :
                            ORDER_ITEM["PAY_SIZE_ID"] = pay_Size(
                                THICKNESS=ORDER_ITEM["PAY_THICKNESS"], WIDTH=ORDER_ITEM["PAY_WIDTH"], LENGTH=ORDER_ITEM["PAY_LENGTH"], ID=request.user.id)
                        #  REQ_SIZE_ID
                        if "REQ_THICKNESS" in ORDER_ITEM and "REQ_WIDTH" in ORDER_ITEM  and "REQ_LENGTH" in ORDER_ITEM :
                            ORDER_ITEM["DLVRY_SIZE_ID"] = pay_Size(
                                THICKNESS=ORDER_ITEM["REQ_THICKNESS"], WIDTH=ORDER_ITEM["REQ_WIDTH"], LENGTH=ORDER_ITEM["REQ_LENGTH"], ID=request.user.id)
                        #   PRODUCT_ID
                        if "PROD_CAT" in ORDER_ITEM and "PROD_NAME" in ORDER_ITEM  and "PROD_USAGE" in ORDER_ITEM :
                            ORDER_ITEM["PRODUCT_ID"] = PRODUCT(
                                CAT_NAME=ORDER_ITEM["PROD_CAT"], PPRO_NAME=ORDER_ITEM["PROD_NAME"], PRO_USAGE=ORDER_ITEM["PROD_USAGE"], ID=request.user.id)
                        # Saving the ORDER_ITEM
                        create_item_serializer = AddOrderItemsSerializer(data=ORDER_ITEM)
                        if create_item_serializer.is_valid():
                            create_item_serializer.save()
                        else:
                            return Response(create_item_serializer.errors, status=400)
            return Response({'success' : "Data is saved successfully" ,  'success_ur' : "ڈیٹا کامیابی سے محفوظ ہو گیا ہے۔" } , status=status.HTTP_201_CREATED)
        return Response(create_serializer.errors, status=400)

    def put(self, request, id=None):
        try:
            order_to_update = Orders.objects.get(ORDR_ID=id, IS_SALE=1)
            order_id = id
        except Orders.DoesNotExist:
            return Response({'error': 'The Sale Order does not exist.' ,  "error_ur" : "سیل آرڈر موجود نہیں ہے۔"}, status=400)
        request.data["IS_SALE"] = 1
        request.data["REC_ADD_BY"] = order_to_update.REC_ADD_BY
        request.data["REC_MOD_BY"] = request.user.id
        try:
            Dict_ORDER_ITEMS = request.data["ORDER_ITEMS"]
        except:
            pass
        # create_order_serializer = OrderSerializer(order_to_update, data=request.data)
        create_order_serializer = AddOrderSerializer(order_to_update, data=request.data)
        if create_order_serializer.is_valid():
            updated_purchase = create_order_serializer.save()
            # Delete Quotations_Items that are not present in the request data
            existing_items = Order_items.objects.filter(ORDR_ID=order_id)
            existing_ids = set(item.ORDR_ITEM_ID for item in existing_items)
            request_ids = set(item.get('ORDR_ITEM_ID') for item in Dict_ORDER_ITEMS)
            ids_to_delete = existing_ids - request_ids
            if ids_to_delete:
                try:
                    quote_items_to_del =  Order_items.objects.filter(ORDR_ITEM_ID__in=ids_to_delete)
                    for quote_item in quote_items_to_del:
                        quote_item.REC_MOD_BY = request.user.id
                        quote_item.IS_ACTIVE = 0
                        quote_item.save()
                except Order_items.DoesNotExist:
                    return Response({'error': 'The Sale Order does not exist.' ,  "error_ur" : "سیل آرڈر موجود نہیں ہے۔"}, status=400)


            for order_item in Dict_ORDER_ITEMS:
                order_item["ORDR_ID"] = order_to_update.ORDR_ID
                order_item["REC_MOD_BY"] = request.user.id
                order_item_id = "ORDR_ITEM_ID"
                if order_item["IS_GEN_PROD"] ==1:
                    # Saving the ORDER_ITEM
                    if order_item_id in order_item:
                        order_Item_to_update = Order_items.objects.get(ORDR_ITEM_ID=order_item["ORDR_ITEM_ID"], ORDR_ID= order_id)                        
                        order_item["REC_ADD_BY"] = order_Item_to_update.REC_ADD_BY 
                        create_item_serializer = AddGeneralOrderItemsSerializer(order_Item_to_update, data=order_item)
                        if create_item_serializer.is_valid():
                            create_item_serializer.save()
                        else:
                            return Response(create_item_serializer.errors, status=400)
                    else:
                        # ADD NEW ORDDER ITEMS
                        create_item_serializer = AddGeneralOrderItemsSerializer(data=order_item)
                        if create_item_serializer.is_valid():
                            create_item_serializer.save()
                        else:
                            return Response(create_item_serializer.errors, status=400)
                else:
                    
                    # UPDATING THE EXISTING ORDDER ITEMS
                    if order_item_id in order_item:
                        #  PAY_SIZE_ID
                        order_item["PAY_SIZE_ID"] = pay_Size(
                            THICKNESS=order_item["PAY_THICKNESS"], WIDTH=order_item["PAY_WIDTH"], LENGTH=order_item["PAY_LENGTH"], ID=request.user.id)
                        #  REQ_SIZE_ID
                        order_item["DLVRY_SIZE_ID"] = pay_Size(
                            THICKNESS=order_item["REQ_THICKNESS"], WIDTH=order_item["REQ_WIDTH"], LENGTH=order_item["REQ_LENGTH"], ID=request.user.id)
                        #  PRODUCT_ID
                        order_item["PRODUCT_ID"] = PRODUCT(
                            CAT_NAME=order_item["PROD_CAT"], PPRO_NAME=order_item["PROD_NAME"], PRO_USAGE=order_item["PROD_USAGE"], ID=request.user.id)
                        # Saving the ORDER_ITEM
                        order_Item_to_update = Order_items.objects.get(ORDR_ITEM_ID=order_item["ORDR_ITEM_ID"], ORDR_ID= order_id )                        
                        order_item["REC_ADD_BY"] = order_Item_to_update.REC_ADD_BY                    
                        if Decimal(order_item["REQ_QTY"]) < order_Item_to_update.DLVRD_QTY:
                            return Response({'errors': 'Delievered Quantity cannot be less than the actual value'}, status=400)
                        if order_item["REQ_QTY"] == order_Item_to_update.DLVRD_QTY:
                            order_item["IS_DLVRD"] = 1
                        else:
                            order_item["IS_DLVRD"] = 0                 
                        update_ordrItem_serializer = AddOrderItemsSerializer(order_Item_to_update, data=order_item)
                        # update_ordrItem_serializer = OrderItemsSerializer(order_Item_to_update, data=order_item)
                        if update_ordrItem_serializer.is_valid():
                            update_ordrItem_serializer.save()
                        else:
                            return Response(create_item_serializer.errors, status=400)
                    else:
                        # ADD NEW ORDDER ITEMS
                        if order_item["IS_GEN_PROD"] ==1:
                            create_item_serializer = AddGeneralOrderItemsSerializer(data=order_item)
                            if create_item_serializer.is_valid():
                                create_item_serializer.save()
                            else:
                                return Response(create_item_serializer.errors, status=400)
                        else:
                            #  PAY_SIZE_ID
                            order_item["PAY_SIZE_ID"] = pay_Size(
                                THICKNESS=order_item["PAY_THICKNESS"], WIDTH=order_item["PAY_WIDTH"], LENGTH=order_item["PAY_LENGTH"], ID=request.user.id)
                            #  REQ_SIZE_ID
                            order_item["DLVRY_SIZE_ID"] = pay_Size(
                                THICKNESS=order_item["REQ_THICKNESS"], WIDTH=order_item["REQ_WIDTH"], LENGTH=order_item["REQ_LENGTH"], ID=request.user.id)
                            #  PRODUCT_ID
                            order_item["PRODUCT_ID"] = PRODUCT(
                                CAT_NAME=order_item["PROD_CAT"], PPRO_NAME=order_item["PROD_NAME"], PRO_USAGE=order_item["PROD_USAGE"], ID=request.user.id)
                            # Saving the ORDER_ITEM
                            order_item["REC_ADD_BY"] = request.user.id
                            create_item_serializer = AddOrderItemsSerializer(data=order_item)
                            # create_item_serializer = OrderItemsSerializer(data=order_item)
                            if create_item_serializer.is_valid():
                                create_item_serializer.save()
                            else:
                                return Response(create_item_serializer.errors, status=400)
            # read_serializer = OrderSerializer(updated_purchase)
            # return Response(read_serializer.data, status=201)
            return Response({'success' : "Order is updated successfully" ,  'success_ur' : "آرڈر کو کامیابی سے اپ ڈیٹ کر دیا گیا ہے۔" } , status=status.HTTP_201_CREATED)
        return Response(create_order_serializer.errors, status=400)

    def delete(self, request, id=None):
        try:
            order_to_delete = Orders.objects.get(ORDR_ID=id, IS_SALE=1)
        except Orders.DoesNotExist:
            return Response({'error': 'The Sale Order does not exist.' ,  "error_ur" : "سیل آرڈر موجود نہیں ہے۔"}, status=400)

        try:
            order_items_to_delete = Order_items.objects.filter(ORDR_ID=id)
        except Orders.DoesNotExist:
            return Response({'error': 'The Sale Order does not exist.' ,  "error_ur" : "سیل آرڈر موجود نہیں ہے۔"}, status=400)

        for order_item in order_items_to_delete:
            if order_item.DLVRD_QTY > 0:
                return Response({'errors': 'Partially or fully delivered orders cannot be changed/deleted.'  ,  "error_ur" : "جزوی طور پر یا مکمل طور پر ڈیلیور کردہ آرڈرز کو تبدیل/حذف نہیں کیا جا سکتا۔"}, status=400)

        order_to_delete.REC_MOD_BY = request.user.id
        order_to_delete.IS_ACTIVE = 0
        order_to_delete.save()

        return Response({'success' : "Order is deleted successfully" ,  'success_ur' : "آرڈر کامیابی کے ساتھ حذف ہو گیا ہے۔" } , status=status.HTTP_200_OK)


class CustomerSaleProductListView(
    APIView,  # Basic View class provided by the Django Rest Framework
    UpdateModelMixin,  # Mixin that allows the basic APIView to handle PUT HTTP requests
    # Mixin that allows the basic APIView to handle DELETE HTTP request):
    DestroyModelMixin,
):


    renderer_classes = [UserRenderer]
    def get(self, request, id=None):
        if id:
            try:
                queryset = Orders.objects.filter(
                    CUST_ACCT_ID=id, IS_ACTIVE=1, IS_SALE=1)
            except Orders.DoesNotExist:
                return Response({'error': 'The Sale Order does not exist.' ,  "error_ur" : "سیل آرڈر موجود نہیں ہے۔"}, status=400)
        read_serializer = MerchantOrderSerializer(queryset, many=True)
        order_item_qs = Order_items.objects.filter(ORDR_ITEM_ID=0)
        for qs in queryset:
            order_item_qs = order_item_qs | qs.ORDER_ITEMS

        order_item_serializer = OrderItemsSerializer(order_item_qs, many=True)

        return Response(order_item_serializer.data, status=200)

    
