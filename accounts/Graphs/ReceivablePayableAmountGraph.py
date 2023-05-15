
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

class ReceivablePayableGraphListView(
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
            query = """ CALL `datafunc_Mabrle_ERP_wUrdu`.`Receiavlble_Payable_Amount_Graph`( 
                        ); """       
            my_data = pd.read_sql(query, connection)
        except ConnectionError:
                return Response({"error" : "Database Connection Error" , "error_ur" :  "ڈیٹا بیس کنکشن کی خرابی " }  , status=status.HTTP_400_BAD_REQUEST)         
        if my_data.empty :
            return Response([], status=status.HTTP_200_OK)
        else:
            my_data = my_data.fillna(0)
            data_set = []
            for index, row in my_data.iterrows():
                data_set.append({           
                        "title": row["ACCT_TITLE"],          
                        "title_ur": row["ACCT_TITLE_UR"],           
                        "subtitle": row["PH_NUM"],           
                        "subtitle_ur": row["PH_NUM"],           
                        "amount": row["CLOSNG_BLNCE"]         
                        })
                   
                
            graph_data = {
                'TITLE': "Receiavlble/Payable Amounts" ,
                'TITLE_UR': "قابل وصول/ قابل ادائیگی رقم" ,
                "DATASET": data_set
                       
            }
            return Response(graph_data, status=status.HTTP_200_OK )        
        
    def get(self, request, id=None):
        return self.searchActive(params=request.query_params)





