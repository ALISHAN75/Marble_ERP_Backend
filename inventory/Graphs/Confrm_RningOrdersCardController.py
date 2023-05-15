from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from accounts.CustomPermission import IsUserAllowed
from accounts.renderers import UserRenderer
# util
import pandas as pd
from django.db import connection
# Utils
from marble_erp.utils.langDetector import lang_detect
from marble_erp.utils.lang_translate import lang_translate


class Confirm_RningOrderCard(
    APIView,  # Basic View class provided by the Django Rest Framework
    UpdateModelMixin,  # Mixin that allows the basic APIView to handle PUT HTTP requests
    # Mixin that allows the basic APIView to handle DELETE HTTP request):
    DestroyModelMixin,
):


    def get(self, request):    
        query = """SELECT sum(case when O.DELVRY_STS = 1 then 1 else 0 end) Closed_Orders
                    , sum(case when O.DELVRY_STS = 0 then 1 else 0 end) All_Open_Orders
                FROM orders O 
                where O.IS_ACTIVE = 1 ;"""
        my_data = pd.read_sql(query, connection)
        query2 = """
        SELECT count(distinct O.ORDR_ID) Partially_Delivered_Orders
                    FROM orders O 
                    join order_items OI on O.ORDR_ID = OI.ORDR_ID
                    where O.IS_ACTIVE = 1 and O.DELVRY_STS = 0 and OI.DLVRD_QTY > 0 
                    """
        my_data2 = pd.read_sql(query2, connection)
        my_data['Partially_Delivered_Orders'] = my_data2
        new_data = [
            {
            'title' : int(my_data['Closed_Orders']),
            'subtitle': lang_translate(stringToConvert= "Closed Orders", from_lang='en', to_lang='ur') , 
        } , 
            {
            'title' : int(my_data['All_Open_Orders']) ,
            'subtitle':  lang_translate(stringToConvert= "All Open Orders", from_lang='en', to_lang='ur') , 
        } , 
            {
            'title' : int(my_data['Partially_Delivered_Orders']) ,
            'subtitle':  lang_translate(stringToConvert= "Partially Delivered Orders", from_lang='en', to_lang='ur') , 
        } , 
            {
            'title' : 5 ,
            'subtitle': lang_translate(stringToConvert= "Quotations", from_lang='en', to_lang='ur') ,  
        } , 
        
        ]

        if my_data.empty or my_data2.empty:
            return Response( {"error" : "No record found" , "error_ur" : "کوئی ریکارڈ نہیں ملا" }, status=400)
        else:
            return Response(new_data, status=200)
