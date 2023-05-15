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




class ProductsInSockGraphListView(
    APIView,  # Basic View class provided by the Django Rest Framework
    UpdateModelMixin,  # Mixin that allows the basic APIView to handle PUT HTTP requests
    # Mixin that allows the basic APIView to handle DELETE HTTP request):
    DestroyModelMixin,
):
    permission_classes = [AllowAny]
    rec_is_active = 1


    def searchActive(self, params):
        
        try:
            query = """ CALL `datafunc_Mabrle_ERP_wUrdu`.`Products_in_Stock_Graph`(1); """       
            prodsInStock = pd.read_sql(query, connection)
        except ConnectionError:
                return Response({"error" : "Database Connection Error" , "error_ur" :  "ڈیٹا بیس کنکشن کی خرابی " }  , status=status.HTTP_400_BAD_REQUEST)         
        if prodsInStock.empty:
            return Response([], status=status.HTTP_200_OK)
        else:
            prodsInStock = prodsInStock.fillna(0)
                
            graph_data = {          
                "TITLE": "Most Products In Stock",       
                "TITLE_UR": "اسٹاک میں سب سے زیادہ مصنوعات",     
                "LABELS": prodsInStock["PROD_NM"] ,    
                "LABELS_UR": prodsInStock["PROD_NM_UR"]   ,   
                 "DATASET": [         
                    {  "data": prodsInStock["AVLBL_SQFT"] }  ] ,
                "DATASET_UR": [          
                    {    "data":  prodsInStock["AVLBL_SQFT"] } ]    
            }

            return Response(graph_data, status=status.HTTP_200_OK )        
        
    def get(self, request, id=None):
        return self.searchActive(params=request.query_params)





