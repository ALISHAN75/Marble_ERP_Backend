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




class CurrentMonthCashGraphListView(
    APIView,  # Basic View class provided by the Django Rest Framework
    UpdateModelMixin,  # Mixin that allows the basic APIView to handle PUT HTTP requests
    # Mixin that allows the basic APIView to handle DELETE HTTP request):
    DestroyModelMixin,
):
    permission_classes = [AllowAny]
    rec_is_active = 1


    def searchActive(self, params):
        try:
            query = """ CALL `datafunc_Mabrle_ERP_wUrdu`.`Current_Month_Cash_Graph`(1); """       
            earning = pd.read_sql(query, connection)
            query = """ CALL `datafunc_Mabrle_ERP_wUrdu`.`Current_Month_Cash_Graph`(2); """       
            expense = pd.read_sql(query, connection)
            query = """ CALL `datafunc_Mabrle_ERP_wUrdu`.`Current_Month_Cash_Graph`(3); """       
            cashinhand = pd.read_sql(query, connection)
        except ConnectionError:
                return Response({"error" : "Database Connection Error" , "error_ur" :  "ڈیٹا بیس کنکشن کی خرابی " }  , status=status.HTTP_400_BAD_REQUEST)         
        if earning.empty and expense.empty and cashinhand.empty:
            return Response([], status=status.HTTP_200_OK)
        else:
            earning = earning.fillna(0)
            expense = expense.fillna(0)
            cashinhand = cashinhand.fillna(0)
                
            graph_data = {          
                "TITLE": "Current Month",     
                "TITLE_UR": "موجودہ مہینہ",     
                "LABELS": ["Cash on Hand", "Earnings", "Expenses"],     
                "LABELS_UR": ["کیش آن ہینڈ", "کمائی", "اخراجات"],     
                "DATASET": [earning["Earning"][0] , expense["Expense"][0] , cashinhand["CashInHand"][0] ],     
                "DATASET_UR": [earning["Earning"][0] , expense["Expense"][0] , cashinhand["CashInHand"][0] ]
            }

            return Response(graph_data, status=status.HTTP_200_OK )        
        
    def get(self, request, id=None):
        return self.searchActive(params=request.query_params)





