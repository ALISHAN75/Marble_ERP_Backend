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


class RevenueIncomeGraphListView(
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
            query = """ CALL `datafunc_Mabrle_ERP_wUrdu`.`Revenue_Graph`(1); """       
            earning = pd.read_sql(query, connection)
            query = """ CALL `datafunc_Mabrle_ERP_wUrdu`.`Revenue_Graph`(2); """       
            expense = pd.read_sql(query, connection)
        except ConnectionError:
                return Response({"error" : "Database Connection Error" , "error_ur" :  "ڈیٹا بیس کنکشن کی خرابی " }  , status=status.HTTP_400_BAD_REQUEST)         
        if earning.empty and expense.empty:
            return Response([], status=status.HTTP_200_OK)
        else:
            earning = earning.fillna(0)
            expense = expense.fillna(0)
                
            graph_data = {
                "TITLE": "Revenue Report",     
                "TITLE_UR": "ریونیو رپورٹ",     
                "DATASET": [         
                {             
                "name": "Earning",             
                "data":          earning["Earning"]           },           
                {             
                "name": "Expense",             
                "data": expense["Expense"]       }                        
                    ],                      
                "DATASET_UR": [         
                {             
                "name": "کمائی",             
                "data":          earning["Earning"]           },           
                {             
                "name": "خرچہ",             
                "data": expense["Expense"]       }                        
                    ],                      
            }
            return Response(graph_data, status=status.HTTP_200_OK )        
        
    def get(self, request, id=None):
        return self.searchActive(params=request.query_params)





