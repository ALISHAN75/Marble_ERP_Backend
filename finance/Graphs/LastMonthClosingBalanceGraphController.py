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




class LastMonthClosingGraphListView(
    APIView,  # Basic View class provided by the Django Rest Framework
    UpdateModelMixin,  # Mixin that allows the basic APIView to handle PUT HTTP requests
    # Mixin that allows the basic APIView to handle DELETE HTTP request):
    DestroyModelMixin,
):
    permission_classes = [AllowAny]
    rec_is_active = 1


    def searchActive(self, params):
        try:
            query = """ CALL `datafunc_Mabrle_ERP_wUrdu`.`Month_closing_balance_graph`(); """       
            cashinhand = pd.read_sql(query, connection)
        except ConnectionError:
                return Response({"error" : "Database Connection Error" , "error_ur" :  "ڈیٹا بیس کنکشن کی خرابی " }  , status=status.HTTP_400_BAD_REQUEST)         
        if cashinhand.empty:
            return Response([], status=status.HTTP_200_OK)
        else:
            cashinhand = cashinhand.fillna(0)             
            graph_data = {   
                    "TITLE": "Closing Balance By Month",     
                    "TITLE_UR": "ماہ کے حساب سے بیلنس بند ",  
                    
                       
                    "DATASET":  {         
                    "labels":  cashinhand["YM"] ,
                    
                    "datasets": {             
                        "data": cashinhand["CashInHand"]                   
                                }  
                    }
                        } 

            return Response(graph_data, status=status.HTTP_200_OK )        
        
    def get(self, request, id=None):
        return self.searchActive(params=request.query_params)





