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
import math
from datetime import datetime
import pandas as pd
from django.db import connection
from inventory.utility.PAY_REQ_SIZE import pay_Size, PRODUCT
from inventory.utility.DataConversion import dateConversion
from accounts.renderers import UserRenderer
# models imports
from inventory.model.Quotations import Quotations, Quotations_Items
from inventory.model.Orders import Orders, Order_items
from inventory.model.ProductSizes import ProductSizes
from accounts.model.Account import Accounts
from finance.model.Earning_Transactions import Earning_Transactions 
# serializers imports
from inventory.serializers.ProductSizesSerializer import ProductSizesSerializer
from inventory.serializers.OrdersSerializer import OrderSerializer, MerchantOrderSerializer , OrderItemsSerializer 
from inventory.serializers.OrderItemsSerializer import OrderItemsSerializer, AddOrderItemsSerializer , AddGeneralQuotationItemsSerializer
from accounts.LedgerTransaction import LedgerTransaction
from finance.serializer.EarningTranscSerializer import AddEarningTranscSerializer
from inventory.serializers.QuotationsSerializer import AddQuotationsSerializer  , QuotationsrSerializer
from inventory.serializers.QuotationsItemsSerializer import AddQuotationsItemsSerializer , QuotationsItemsSerializer 

class QuotationsListView(
    APIView,  # Basic View class provided by the Django Rest Framework
    UpdateModelMixin,  # Mixin that allows the basic APIView to handle PUT HTTP requests
    # Mixin that allows the basic APIView to handle DELETE HTTP request):
    DestroyModelMixin,
):
    permission_classes = [IsUserAllowed({'POST': 'inventory.add_orders', 'PUT': 'inventory.change_orders',
                                        'DELETE': 'inventory.delete_orders', 'GET': 'inventory.view_orders'})]
    rec_is_active = 1
    renderer_classes = [UserRenderer]
    
             
    def getOne(self, request, id):
        if id:
            try:
                query = """ CALL `datafunc_Mabrle_ERP_wUrdu`.`Quotation_List`("""+str(id)+""", 1, "", 1, 1000000); """     
                orders = pd.read_sql(query, connection)
                query = """CALL `datafunc_Mabrle_ERP_wUrdu`.`Quotation_Detail`( 1 , """+str(id)+""");  """    
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
            query = """ CALL `datafunc_Mabrle_ERP_wUrdu`.`Quotation_List`(0, 1, "", 1, 1000000); """    
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
            query = """ CALL `datafunc_Mabrle_ERP_wUrdu`.`Quotation_List`(0, 1, '"""+q+"""', """+str(page)+""", """+str(parPage)+"""); """       
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
        request.data["REC_ADD_BY"] = request.user.id
        request.data["REC_MOD_BY"] = request.user.id
        # request.data["IS_SALE"] = 1
        try:
            Dict_QUOTATIONS_ITEMS = request.data["ORDER_ITEMS"]
        except:
            pass
        create_serializer = AddQuotationsSerializer(data=request.data)
        if create_serializer.is_valid():
            new_sale = create_serializer.save()
            if len(Dict_QUOTATIONS_ITEMS) > 0:
                for ORDER_ITEM in Dict_QUOTATIONS_ITEMS:
                    ORDER_ITEM["QUOTE_ID"] = new_sale.QUOTE_ID
                    ORDER_ITEM["REC_ADD_BY"] = request.user.id
                    ORDER_ITEM["REC_MOD_BY"] = request.user.id
                    if ORDER_ITEM["IS_GEN_PROD"] ==1:
                        create_item_serializer = AddGeneralQuotationItemsSerializer(data=ORDER_ITEM)
                        if create_item_serializer.is_valid():
                            create_item_serializer.save()
                        else:
                            return Response(create_item_serializer.errors, status=400)
                    else:
                        #  PAY_SIZE_ID
                        ORDER_ITEM["PAY_SIZE_ID"] = pay_Size(
                            THICKNESS=ORDER_ITEM["PAY_THICKNESS"], WIDTH=ORDER_ITEM["PAY_WIDTH"], LENGTH=ORDER_ITEM["PAY_LENGTH"], ID=request.user.id)
                        #   REQ_SIZE_ID
                        ORDER_ITEM["DLVRY_SIZE_ID"] = pay_Size(
                            THICKNESS=ORDER_ITEM["REQ_THICKNESS"], WIDTH=ORDER_ITEM["REQ_WIDTH"], LENGTH=ORDER_ITEM["REQ_LENGTH"], ID=request.user.id)
                        #   PRODUCT_ID
                        ORDER_ITEM["PRODUCT_ID"] = PRODUCT(
                            CAT_NAME=ORDER_ITEM["PROD_CAT"], PPRO_NAME=ORDER_ITEM["PROD_NAME"], PRO_USAGE=ORDER_ITEM["PROD_USAGE"], ID=request.user.id)
                        # Saving the ORDER_ITEM
                        create_item_serializer = AddQuotationsItemsSerializer(data=ORDER_ITEM)
                        if create_item_serializer.is_valid():
                            create_item_serializer.save()
                        else:
                            return Response(create_item_serializer.errors, status=400)
            # read_serializer = QuotationsrSerializer(new_sale)
            # return Response(read_serializer.data, status=201)
            return Response({'success' : "Data is saved successfully" ,  'success_ur' : "ڈیٹا کامیابی سے محفوظ ہو گیا ہے۔" } , status=status.HTTP_201_CREATED)
        return Response(create_serializer.errors, status=400)


    def put(self, request, id=None):
        try:
            order_to_update = Quotations.objects.get(QUOTE_ID=id)
            quote_id = id
        except Orders.DoesNotExist:
             return Response({'error': 'This Quotations Order does not exist.' ,  "error_ur" : "یہ کوٹیشن آرڈر موجود نہیں ہے۔"}, status=400)
        request.data["IS_NOW_ORDER"] = 1
        request.data["REC_ADD_BY"] = order_to_update.REC_ADD_BY
        request.data["REC_MOD_BY"] = request.user.id
        try:
            Dict_ORDER_ITEMS = request.data["ORDER_ITEMS"]
        except:
            pass
        create_order_serializer = AddQuotationsSerializer(order_to_update, data=request.data)
        if create_order_serializer.is_valid():
            updated_purchase = create_order_serializer.save()

            # Delete Quotations_Items that are not present in the request data
            existing_items = Quotations_Items.objects.filter(QUOTE_ID=quote_id)
            existing_ids = set(item.QUOTE_ITEM_ID for item in existing_items)
            request_ids = set(item.get('QUOTE_ITEM_ID') for item in Dict_ORDER_ITEMS)
            ids_to_delete = existing_ids - request_ids
            if ids_to_delete:
                try:
                    quote_items_to_del =  Quotations_Items.objects.filter(QUOTE_ITEM_ID__in=ids_to_delete)
                    for quote_item in quote_items_to_del:
                        quote_item.REC_MOD_BY = request.user.id
                        quote_item.IS_ACTIVE = 0
                        quote_item.save()
                except Quotations_Items.DoesNotExist:
                    return Response({'error': 'This Quotations_Items does not exist.' ,  "error_ur" : "یہ کوٹیشن آرڈر موجود نہیں ہے۔"}, status=400)

            # Updating or adding new Quotations Items
            for order_item in Dict_ORDER_ITEMS:
                order_item["QUOTE_ID"] = updated_purchase.QUOTE_ID
                order_item["REC_MOD_BY"] = request.user.id
                order_item_id = "QUOTE_ITEM_ID"
                if order_item["IS_GEN_PROD"] ==1:
                    # Saving the ORDER_ITEM
                    if order_item_id in order_item:
                        order_Item_to_update = Quotations_Items.objects.get(QUOTE_ITEM_ID=order_item["QUOTE_ITEM_ID"], QUOTE_ID=quote_id)                        
                        order_item["REC_ADD_BY"] = order_Item_to_update.REC_ADD_BY 
                        create_item_serializer = AddGeneralQuotationItemsSerializer(order_Item_to_update, data=order_item)
                        if create_item_serializer.is_valid():
                            create_item_serializer.save()
                        else:
                            return Response(create_item_serializer.errors, status=400)
                    else:
                        # ADD NEW ORDDER ITEMS
                        create_item_serializer = AddGeneralQuotationItemsSerializer(data=order_item)
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
                        order_Item_to_update = Quotations_Items.objects.get(QUOTE_ITEM_ID=order_item["QUOTE_ITEM_ID"], QUOTE_ID=quote_id)                        
                        order_item["REC_ADD_BY"] = order_Item_to_update.REC_ADD_BY                    
                        
                        update_ordrItem_serializer = AddQuotationsItemsSerializer(order_Item_to_update, data=order_item)
                        # update_ordrItem_serializer = OrderItemsSerializer(order_Item_to_update, data=order_item)
                        if update_ordrItem_serializer.is_valid():
                            update_ordrItem_serializer.save()
                        else:
                            return Response(create_item_serializer.errors, status=400)
                    else:
                        # ADD NEW ORDDER ITEMS
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

                        create_item_serializer = AddQuotationsItemsSerializer(data=order_item)
                        # create_item_serializer = OrderItemsSerializer(data=order_item)
                        if create_item_serializer.is_valid():
                           temp =  create_item_serializer.save()
                        else:
                            return Response(create_item_serializer.errors, status=400)
            # read_serializer = QuotationsrSerializer(updated_purchase)
            # return Response(read_serializer.data, status=201)
            return Response({'success' : "Data is saved successfully" ,  'success_ur' : "ڈیٹا کامیابی سے محفوظ ہو گیا ہے۔" } , status=status.HTTP_201_CREATED)
        return Response(create_order_serializer.errors, status=400)





    def delete(self, request, id=None):
        try:
            order_to_delete = Quotations.objects.get(QUOTE_ID=id)
        except Quotations.DoesNotExist:
            return Response({'error': 'This Quotations Order does not exist.' ,  "error_ur" : "یہ کوٹیشن آرڈر موجود نہیں ہے۔"}, status=400)

        order_to_delete.REC_MOD_BY = request.user.id
        order_to_delete.IS_ACTIVE = 0
        order_to_delete.save()

        return Response({'success' : "Data is deleted successfully" ,  'success_ur' : "ڈیٹا کامیابی سے حذف ہو گیا ہے۔" } , status=status.HTTP_200_OK)

