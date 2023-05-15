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




class MonthlyCashGraphListView(
    APIView,  # Basic View class provided by the Django Rest Framework
    UpdateModelMixin,  # Mixin that allows the basic APIView to handle PUT HTTP requests
    # Mixin that allows the basic APIView to handle DELETE HTTP request):
    DestroyModelMixin,
):
    permission_classes = [AllowAny]
    rec_is_active = 1


    def searchActive(self, params):
        try:
            query = """ CALL `datafunc_Mabrle_ERP_wUrdu`.`Monthly_Cash_Graph`(1); """       
            earning = pd.read_sql(query, connection)
            query = """ CALL `datafunc_Mabrle_ERP_wUrdu`.`Monthly_Cash_Graph`(2); """       
            expense = pd.read_sql(query, connection)
            query = """ CALL `datafunc_Mabrle_ERP_wUrdu`.`Monthly_Cash_Graph`(3); """       
            cashinhand = pd.read_sql(query, connection)
            query = """ CALL `datafunc_Mabrle_ERP_wUrdu`.`Monthly_Cash_Graph`(4); """       
            latestcashinhand = pd.read_sql(query, connection)
        except ConnectionError:
                return Response({"error" : "Database Connection Error" , "error_ur" :  "ڈیٹا بیس کنکشن کی خرابی " }  , status=status.HTTP_400_BAD_REQUEST)         
        if earning.empty and expense.empty:
            return Response([], status=status.HTTP_200_OK)
        else:
            earning = earning.fillna(0)
            expense = expense.fillna(0)
            latestcashinhand = latestcashinhand.fillna(0)
            cashinhand = cashinhand.fillna(0)
                
            graph_data = {          
                "TITLE": latestcashinhand["BALANCE"][0],       
                "TITLE_UR": latestcashinhand["BALANCE"][0],     
                "SUBTITLE": "",     
                "SUBTITLE_UR": "",     
                "LABELS": earning["YM"] ,    
                "LABELS_UR": earning["YM"]   ,   
                "DATASET": [         
{           "label": "Earning",           "data": earning["Earning"]        },         
{           "label": "Expense",           "data": expense["Expense"]          },         
{           "label": "Cash in Hand",       "data": cashinhand["CashInHand"]          }       ],
            "DATASET_UR": [         
{           "label": "کمائی",           "data": earning["Earning"]         },         
{           "label": "خرچہ",           "data": expense["Expense"]        },         
{           "label": "کیش ان ہینڈ",       "data": cashinhand["CashInHand"]         }       ],
            }

            return Response(graph_data, status=status.HTTP_200_OK )        
        
    def get(self, request, id=None):
        return self.searchActive(params=request.query_params)





