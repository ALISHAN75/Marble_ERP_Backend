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




class DashboardCardRevenueSummaryListView(
    APIView,  # Basic View class provided by the Django Rest Framework
    UpdateModelMixin,  # Mixin that allows the basic APIView to handle PUT HTTP requests
    # Mixin that allows the basic APIView to handle DELETE HTTP request):
    DestroyModelMixin,
):
    permission_classes = [AllowAny]
    # renderer_classes = [UserRenderer]
    rec_is_active = 1


    def searchActive(self, params):
        try:
            query = """ CALL `datafunc_Mabrle_ERP_wUrdu`.`Dashboard_Card_Revenue_Summary`(1); """       
            earning = pd.read_sql(query, connection)
            query = """ CALL `datafunc_Mabrle_ERP_wUrdu`.`Dashboard_Card_Revenue_Summary`(2); """       
            expense = pd.read_sql(query, connection)
            query = """ CALL `datafunc_Mabrle_ERP_wUrdu`.`Dashboard_Card_Revenue_Summary`(3); """       
            profit = pd.read_sql(query, connection)
            query = """ CALL `datafunc_Mabrle_ERP_wUrdu`.`Dashboard_Card_Revenue_Summary`(4); """       
            cashinhand = pd.read_sql(query, connection)
        except ConnectionError:
                return Response({"error" : "Database Connection Error" , "error_ur" :  "ڈیٹا بیس کنکشن کی خرابی " }  , status=status.HTTP_400_BAD_REQUEST)         
        if earning.empty and expense.empty:
            return Response([], status=status.HTTP_200_OK)
        else:
            earning = earning.fillna(0)
            expense = expense.fillna(0)
            profit = profit.fillna(0)
            CashLedger = cashinhand.fillna(0)
                
            graph_data = [ {          
                "title": "Profit",         
                "title_ur": "منافع",         
                "statistics": "",          
                "series":[{ "data": profit["profit"]  }]      
                },     
                
                {          
                "title": "Cash in Hand",         
                "title_ur": "کیش ان ہینڈ",         
                "statistics": "",          
                "series":[{ "data": cashinhand["CashInHand"]  }]      
                },  
                {          
                "title": "Monthly Earning",         
                "title_ur": "ماہانہ کمائی",         
                "statistics": "",          
                "series":[{ "data": earning["Earning"]   }]      
                },     

                {          
                "title": "Monthly Expense",         
                "title_ur": "ماہانہ خرچہ",         
                "statistics": "",          
                "series":[{ "data": expense["Expense"]  }]      
                }
                ]

            return Response(graph_data, status=status.HTTP_200_OK )        
        
    def get(self, request, id=None):
        return self.searchActive(params=request.query_params)





