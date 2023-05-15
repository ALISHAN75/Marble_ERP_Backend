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
import pandas as pd
from django.db import connection




class TopImportedProductsGraphListView(
    APIView,  # Basic View class provided by the Django Rest Framework
    UpdateModelMixin,  # Mixin that allows the basic APIView to handle PUT HTTP requests
    # Mixin that allows the basic APIView to handle DELETE HTTP request):
    DestroyModelMixin,
):
    permission_classes = [AllowAny]
    rec_is_active = 1


    def searchActive(self, params):
        
        try:
            query = """ CALL `datafunc_Mabrle_ERP_wUrdu`.`Top_Imported_exported_products_Graph`(2 , 0); """       
            QuantityImported = pd.read_sql(query, connection)
        except ConnectionError:
                return Response({"error" : "Database Connection Error" , "error_ur" :  "ڈیٹا بیس کنکشن کی خرابی " }  , status=status.HTTP_400_BAD_REQUEST)         
        if QuantityImported.empty:
            return Response([], status=status.HTTP_200_OK)
        else:
            QuantityImported = QuantityImported.fillna(0)
                
            graph_data = {          
                "TITLE": "Top sold purchase products",       
                "TITLE_UR": "سب سے زیادہ فروخت شدہ خریداری کی مصنوعات",     
                "SUB_TITLE": "",     
                "SUB_TITLE_UR": "",     
                "LABELS": QuantityImported["PROD_NM"] ,    
                "LABELS_UR": QuantityImported["PROD_NM_UR"]   ,   
                 "DATASET": [         
                    {    "label": "Quantity Imported SQTY",            "data": QuantityImported["PROD_QTY_SQFT"] }  ] ,
                "DATASET_UR": [          
                    {    "label": "درآمد شدہ مقدار",               "data":  QuantityImported["PROD_QTY_SQFT"] } ]    
            }

            return Response(graph_data, status=status.HTTP_200_OK )        
        
    def get(self, request, id=None):
        return self.searchActive(params=request.query_params)





