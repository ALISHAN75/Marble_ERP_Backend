
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


class InevntoryTransactionGraphListView(
    APIView,  # Basic View class provided by the Django Rest Framework
    UpdateModelMixin,  # Mixin that allows the basic APIView to handle PUT HTTP requests
    # Mixin that allows the basic APIView to handle DELETE HTTP request):
    DestroyModelMixin,
):
    permission_classes = [AllowAny]
    # renderer_classes = [UserRenderer]
    rec_is_active = 1


    def searchActive(self, params):
        data_Type = params.get('data_Type' ,'')
        try:
            query = """ CALL `datafunc_Mabrle_ERP_wUrdu`.`Inevntory_Transaction_Graph`( 
                            '"""+str(data_Type)+"""'
                                ); """       
            my_data = pd.read_sql(query, connection) 
        except ConnectionError:
                return Response({"error" : "Database Connection Error" , "error_ur" :  "ڈیٹا بیس کنکشن کی خرابی " }  , status=status.HTTP_400_BAD_REQUEST)         
        if my_data.empty :
            return Response([], status=status.HTTP_200_OK)
        else:
            my_data = my_data.fillna(0)
            graph_data = {
                'TITLE': my_data["TITLE"][0] ,
                'TITLE_UR': my_data["TITLE_UR"][0] ,
                "DATASET": [        
                        {           
                        "name": "Time_Period",            
                        "data": my_data["Time_Period"]        
                        },         
                        {    
                        "name": "TRANS_TYP" ,          
                        "data": my_data["TRANS_TYP"]      
                        } ,      
                        {           
                        "name": "TRANS_TYP_UR" ,          
                        "data": my_data["TRANS_TYP_UR"]        
                        },         
                        {    
                        "name": "TRANS_COST" ,        
                        "data": my_data["TRANS_COST"]      
                        }      
                 ]
            }
            return Response(graph_data, status=status.HTTP_200_OK  )        
        
    def get(self, request, id=None):
        if request.query_params:
            return self.searchActive(params=request.query_params)
        else:
            return  Response({"error" : "Provide for parameters for searching" , "error_ur" : "تلاش کے لیے پیرامیٹرز فراہم کریں۔"}  , status=status.HTTP_400_BAD_REQUEST ) 



