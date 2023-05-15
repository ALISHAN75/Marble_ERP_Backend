
from django.db.models import Q
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework import filters
from rest_framework.permissions import AllowAny
from accounts.renderers import UserRenderer
# Utils
from marble_erp.utils.langDetector import lang_detect
from marble_erp.utils.lang_translate import lang_translate
from inventory.utility.DataConversion import dateConversion
import pandas as pd
from django.db import connection
import math
from inventory.utility.Translation import func_en_to_ur , func_ur_to_en
# models imports
from accounts.model.CashLedger import CashLedger
# serializers imports
from accounts.serializer.CashLedgerSerializer import AddCashLedgerSerializer, CashLedgerSerializer


class AccountTopProductGraphListView(
    APIView,  # Basic View class provided by the Django Rest Framework
    UpdateModelMixin,  # Mixin that allows the basic APIView to handle PUT HTTP requests
    # Mixin that allows the basic APIView to handle DELETE HTTP request):
    DestroyModelMixin,
):
    permission_classes = [AllowAny]
    # renderer_classes = [UserRenderer]
    rec_is_active = 1


    def searchActive(self, params):
        ACCT_ID = params.get('ACCT_ID' , 0)
        try:
            query = """ CALL `datafunc_Mabrle_ERP_wUrdu`.`Top_Product_Graph`( 
                            """+str(ACCT_ID)+"""
                                ); """       
            top_products = pd.read_sql(query, connection)         
        except ConnectionError:
                return Response({"error" : "Database Connection Error" , "error_ur" :  "ڈیٹا بیس کنکشن کی خرابی " }  , status=status.HTTP_400_BAD_REQUEST)         
        if top_products.empty :
            return Response([], status=status.HTTP_200_OK)
        else:
            top_products = top_products.fillna(0)
            graph_data = {   
                    "TITLE": "Top 3 Sale/Purchase Products",   
                    "TITLE_UR": "سرفہرست 3 فروخت/خریداری مصنوعات",   
                    "SUB_TITLE":  top_products["PROD_TOTL_PRICE"].sum(),   
                    "SUB_TITLE_UR":  top_products["PROD_TOTL_PRICE"].sum(),   
                    "LABELS": top_products["PROD_NM"],   
                    "LABELS_UR": top_products["PROD_NM_UR"],  
                    "DATASET": top_products["PROD_QTY"],   
                    "SUMMARY_KEY": "Amount",  
                    "SUMMARY_VALUE": top_products["PROD_TOTL_PRICE"].sum() 
                }
            return Response(graph_data, status=status.HTTP_200_OK , )        
        
    def get(self, request, id=None):
        if request.query_params:
            return self.searchActive(params=request.query_params)
        else:
            return  Response({"error" : "Provide for parameters for searching" , "error_ur" : "تلاش کے لیے پیرامیٹرز فراہم کریں۔"}  , status=status.HTTP_400_BAD_REQUEST ) 



