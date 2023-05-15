
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


class AccountGraphListView(
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
        start_date = params.get('start_date' , '01/01/1969') 
        end_date = params.get('end_date'  ,    '31/12/2099')
        start_date = dateConversion(start_date)
        end_date = dateConversion(end_date)
        try:
            query = """ CALL `datafunc_Mabrle_ERP_wUrdu`.`ACCT_Cust_Graph`(1, 
                            """+str(ACCT_ID)+"""
                            , '"""+start_date+"""'
                            , '"""+end_date+"""'
                            ); """       
            closing_blnc = pd.read_sql(query, connection)
            query = """ CALL `datafunc_Mabrle_ERP_wUrdu`.`ACCT_Cust_Graph`(2, 
                            """+str(ACCT_ID)+"""
                            , '"""+start_date+"""'
                            , '"""+end_date+"""'
                            ); """       
            sale_amount = pd.read_sql(query, connection)
 
        except ConnectionError:
                return Response({"error" : "Database Connection Error" , "error_ur" :  "ڈیٹا بیس کنکشن کی خرابی " }  , status=status.HTTP_400_BAD_REQUEST)         
        if sale_amount.empty :
            return Response([], status=status.HTTP_200_OK)
        else:
            sale_amount = sale_amount.fillna(0)
            graph_data = {
                'TITLE': closing_blnc["BALANCE_TYPE"][0] ,
                'TITLE_UR': closing_blnc["BALANCE_TYPE_UR"][0] ,
                'SUB_TITLE': closing_blnc.iloc[0,0] ,
                'SUB_TITLE_UR': closing_blnc.iloc[0,0],
                'LABELS':sale_amount["YM"] ,
                'LABELS_UR':sale_amount["YM_UR"] ,
                "DATASET": [        
                        {           
                        "label": "CREDIT_AMT",           
                        "data": sale_amount["CREDIT_AMT"]        
                        },         
                        {    
                        "label": "RECEIVED_AMT",          
                        "data": sale_amount["RECEIVED_AMT"]      
                        } ,      
                        {           
                        "label": "DEBIT_AMT",           
                        "data": sale_amount["DEBIT_AMT"]        
                        },         
                        {    
                        "label": "PAID_AMT",          
                        "data": sale_amount["PAID_AMT"]      
                        }      
                 ] , 
                "DATASET_UR": [        
                        {           
                        "label": "کریڈٹ کی رقم",           
                        "data": sale_amount["CREDIT_AMT"]        
                        },         
                        {    
                        "label": "وصول شدہ رقم",          
                        "data": sale_amount["RECEIVED_AMT"]      
                        } ,      
                        {           
                        "label": "ڈیبٹ کی رقم",           
                        "data": sale_amount["DEBIT_AMT"]        
                        },         
                        {    
                        "label": "ادا شدہ رقم",          
                        "data": sale_amount["PAID_AMT"]      
                        }      
                 ]
            }
            return Response(graph_data, status=status.HTTP_200_OK , )        
        
    def get(self, request, id=None):
        if request.query_params:
            return self.searchActive(params=request.query_params)
        else:
            return  Response({"error" : "Provide for parameters for searching" , "error_ur" : "تلاش کے لیے پیرامیٹرز فراہم کریں۔"}  , status=status.HTTP_400_BAD_REQUEST ) 





