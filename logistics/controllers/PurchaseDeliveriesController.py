from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from accounts.CustomPermission import IsUserAllowed
from rest_framework import status
from decimal import Decimal
import math
from datetime import datetime
from accounts.renderers import UserRenderer
# util
import pandas as pd
from django.db import connection
from inventory.utility.DataConversion import dateConversion
# models imports
from inventory.model.ProductSizes import ProductSizes
from inventory.utility.OrderUtil import OrderUtil
from logistics.model.Deliveries import Deliveries, Delivery_Items
# serializers imports
from logistics.serializer.DeliveriesSerializer import DeliveriesDetailSerializer, AddDeliverySerializer
from logistics.serializer.DeliveryItemsSerializer import AddDeliveryItemSerializer, DeliveryItemsSerializer
from logistics.utility.DeliveryUtil import DeliveryUtil
# Utils
from marble_erp.utils.langDetector import lang_detect
from marble_erp.utils.lang_translate import lang_translate


class PurchaseDeliveriesListView(
    APIView,  # Basic View class provided by the Django Rest Framework
    UpdateModelMixin,  # Mixin that allows the basic APIView to handle PUT HTTP requests
    # Mixin that allows the basic APIView to handle DELETE HTTP request):
    DestroyModelMixin,
):
    permission_classes = [IsUserAllowed({'POST': 'logistics.add_deliveries', 'PUT': 'logistics.change_deliveries',
                                        'DELETE': 'logistics.delete_deliveries', 'GET': 'logistics.view_deliveries'})]
    renderer_classes = [UserRenderer]
    rec_is_active = 1
    # deliveryUtil
    deliveryUtil = None


    def getOne(self, request, id):
        if id:
            try:
                query = """ CALL `datafunc_Mabrle_ERP_wUrdu`.`LOGISTICS_DeliveriesList`( 1 , 0 , """+str(id)+""" , 0 , '1969-01-01'  , '2099-12-31' ,  1, 1 ); """     
                orders = pd.read_sql(query, connection)
                query = """ CALL `datafunc_Mabrle_ERP_wUrdu`.`LOGISTICS_DeliveriesList`( 4 , 0 , """+str(id)+""", 0 , '1969-01-01'  , '2099-12-31' ,  1, 1); """    
                orders_items_data = pd.read_sql(query, connection)
            except ConnectionError:
                return Response({"error" : "Database Connection Error" , "error_ur" :  "ڈیٹا بیس کنکشن کی خرابی " }, status=status.HTTP_400_BAD_REQUEST)

        if orders.empty:
            return Response({"error" : "No record found" , "error_ur" : "کوئی ریکارڈ نہیں ملا" }, status=status.HTTP_400_BAD_REQUEST)
        else:
            orders = orders.fillna('')
            orders_items_data = orders_items_data.fillna('')
            orders_data=orders.to_dict(orient='records')[0]
            orders_data['DELIVERY_ITEMS'] = orders_items_data.to_dict(orient='records')
            return Response(orders_data  , status=status.HTTP_200_OK)

             

    def getAll(self):
        try:
            query = """ CALL `datafunc_Mabrle_ERP_wUrdu`.`LOGISTICS_DeliveriesList`(2, 0, 1 , 0 , '1969-01-01'  , '2099-12-31' ,  1, 1000000); """    
            my_data = pd.read_sql(query, connection)
        except ConnectionError:
            return Response({"error" : "Database Connection Error" , "error_ur" :  "ڈیٹا بیس کنکشن کی خرابی " }, status=status.HTTP_400_BAD_REQUEST)
        if my_data.empty:
            return Response({"error" : "No record found" , "error_ur" : "کوئی ریکارڈ نہیں ملا" }, status=status.HTTP_400_BAD_REQUEST)
        else:
            my_data = my_data.fillna('')
            return Response(my_data.to_dict(orient='records'), status=status.HTTP_200_OK)

    def searchActive(self, params):
        is_id_srch = 0
        page = int(params.get('page' , 1) ) 
        parPage = params.get('perPage' , 10)
        start_date = params.get('start_date' , '01/01/1969') 
        end_date = params.get('end_date'  ,    '31/12/2099')
        ACCT_ID = params.get('ACCT_ID' , 0)
        q = params.get('q', '') 
        start_date = dateConversion(start_date)
        end_date = dateConversion(end_date)
        if len(q)>0:
            is_id_srch = 3
            q = dateConversion(q)
        else:
            is_id_srch = 2
        try:
            query = """ CALL `datafunc_Mabrle_ERP_wUrdu`.`LOGISTICS_DeliveriesList`("""+str(is_id_srch)+""" , 0, '"""+q+"""' , """+str(ACCT_ID)+""",  '"""+start_date+"""', '"""+end_date+"""'  , """+str(page)+""", """+str(parPage)+"""); """       
            my_data = pd.read_sql(query, connection)
            query = """ select FOUND_ROWS() """       
            total = pd.read_sql(query, connection)
        except ConnectionError:
                return Response({"error" : "Database Connection Error" , "error_ur" :  "ڈیٹا بیس کنکشن کی خرابی " }, status=status.HTTP_400_BAD_REQUEST)
        
        if my_data.empty:
            return Response([], status=status.HTTP_200_OK)
            # return Response({"error" : "No record found" , "error_ur" : "کوئی ریکارڈ نہیں ملا" }, status=status.HTTP_400_BAD_REQUEST)
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

    def getProductItemVolume(self, delivery, deliveryItems, orderUtil):
        totalVolume = Decimal(0)
        productItemVolume = []
        for delivery_item in deliveryItems:
            orderItem = delivery_item["ORDR_ITEM_ID"]
            ordrItem_qs = orderUtil.findOrderItem(
                order_item_id=orderItem)
            productSize = ProductSizes.objects.get(
                SIZE_ID=ordrItem_qs.DLVRY_SIZE_ID.SIZE_ID)

            dimensions = productSize.LENGHT * \
                productSize.WIDTH * (productSize.THICKNESS / 8)
            qty = round(Decimal(delivery_item["PROD_QTY"]), 2)
            volume = dimensions * qty

            productItemVolume.append(volume)
            totalVolume = totalVolume + volume
        return totalVolume, productItemVolume

    def insertDeliveryItem(self, delivery, deliveryItems, deliveryCost, user):
        orderUtil = OrderUtil()
        self.deliveryUtil = DeliveryUtil()
        order_amount = 0

        totalVolume, productItemVolume = self.deliveryUtil.getProductItemVolume(
            deliveryItems=deliveryItems, orderUtil=orderUtil)

        for index, delivery_item in enumerate(deliveryItems):
            delivery_item["DLVRY_ID"] = delivery.DLVRY_ID
            delivery_item["REC_ADD_BY"] = user.id
            delivery_item["REC_MOD_BY"] = user.id
            orderItem = delivery_item["ORDR_ITEM_ID"]

            create_item_serializer = AddDeliveryItemSerializer(
                data=delivery_item)
            create_item_serializer.is_valid(raise_exception=True)
            delivery_item_rec = create_item_serializer.save()
            ordrItem_to_update = orderUtil.findOrderItem(
                order_item_id=orderItem)

            if ordrItem_to_update is not None:
                self.deliveryUtil.calcCostPerUnitDelQty(
                    deliveryItem=delivery_item_rec, deliveryCost=deliveryCost, productItemVolume=productItemVolume[index], totalVolume=totalVolume)
                order_amount = orderUtil.updateOrderQty(
                    orderItem=ordrItem_to_update, deliveryItemRec=delivery_item_rec, orderAmount=order_amount)
                deliveryItem = self.deliveryUtil.saveUnitPriceWDelivery(
                    deliveryItem=delivery_item_rec, orderItem=ordrItem_to_update)
                
        return order_amount

    def post(self, request):
        request.data["REC_ADD_BY"] = request.user.id
        request.data["REC_MOD_BY"] = request.user.id
        request.data["IS_SALE"] = 0

        create_serializer = AddDeliverySerializer(
            data=request.data, context={'request': request})
        if create_serializer.is_valid():
            new_delivery = create_serializer.save()
            deliveryCost = round(
                new_delivery.EXTRAS_COST + new_delivery.LOAD_COST + new_delivery.RENT_COST, 2)
            order_amount = self.insertDeliveryItem(
                delivery=new_delivery,  deliveryItems=request.data["DELIVERY_ITEMS"], deliveryCost=deliveryCost, user=request.user)
            

            new_delivery.DLVRY_COST = deliveryCost
            new_delivery.DLVRY_ORDR_COST = round(Decimal(order_amount), 2)
            new_delivery.DLVRY_wORDR_COST = round(
                Decimal(order_amount) + Decimal(deliveryCost), 2)
            new_delivery.save()

            # update Parent Order Table
            # self.deliveryUtil.updateOrderStatus(orderIdToUpdate=new_delivery.ORDR_ID.ORDR_ID)

            # read_serializer = DeliveriesDetailSerializer(new_delivery)
            return Response({
                "success": "Delivery is Added successfully",
                "success_ur": "ڈیلیوری کامیابی کے ساتھ شامل کر دی گئی ہے۔"
            }, status=status.HTTP_201_CREATED)
        return Response(create_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

