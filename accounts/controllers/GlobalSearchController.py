
from django.db.models import Q
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework import filters
from rest_framework.permissions import AllowAny
from accounts.renderers import UserRenderer
from inventory.utility.DataConversion import dateConversion
import pandas as pd
from django.db import connection
import math
# models imports
from accounts.model.AcctLedger import Acct_Ledger

# serializers imports
from accounts.serializer.AcctLedgerSerializer import AcctLedgerSerializer, AddAcctLedgerSerializer


class GlobalSearchListView(
    APIView,  # Basic View class provided by the Django Rest Framework
    UpdateModelMixin,  # Mixin that allows the basic APIView to handle PUT HTTP requests
    # Mixin that allows the basic APIView to handle DELETE HTTP request):
    DestroyModelMixin,
):
    permission_classes = [AllowAny]
    renderer_classes = [UserRenderer]
    rec_is_active = 1


    def searchActive(self, params):
        page =   params.get('page' , 1) 
        parPage = params.get('perPage' , 10)
        ORDR_ID = params.get('ORDR_ID' , 0)
        DLVRY_ID = params.get('DLVRY_ID' , 0)
        INVNTRY_TRANS_ID = params.get('INVNTRY_TRANS_ID' , 0)
        EARN_TRANS_ID = params.get('EARN_TRANS_ID' , 0)
        EXPNS_TRANS_ID = params.get('EXPNS_TRANS_ID' , 0)
        TASK_ID = params.get('TASK_ID' , 0)
        ACCT_ID = params.get('ACCT_ID' , 0) 
        try:
            query = """ CALL datafunc_Mabrle_ERP_wUrdu.`General_Search`(
                            """+str(page)+"""           #Starting Page
                            , """+str(parPage)+"""          #parPage
                            , """+str(ORDR_ID)+"""          #ORDR_ID
                            , """+str(DLVRY_ID)+"""          #DLVRY_ID
                            , """+str(INVNTRY_TRANS_ID)+"""  #INVNTRY_TRANS_ID
                            , """+str(EARN_TRANS_ID)+"""   #EARN_TRANS_ID
                            , """+str(EXPNS_TRANS_ID)+"""  #EXPNS_TRANS_ID
                            , """+str(TASK_ID)+"""         #TASK_ID
                            , """+str(ACCT_ID)+"""         #ACCT_ID
                            );
                            """       
            my_data = pd.read_sql(query, connection)
            query = """ select FOUND_ROWS() """       
            total = pd.read_sql(query, connection)
        except ConnectionError:
                return Response( {"error" : "Database Connection Error" , "error_ur" :  "ڈیٹا بیس کنکشن کی خرابی " }, status=status.HTTP_400_BAD_REQUEST)     
        if my_data.empty:
            return Response([], status=status.HTTP_200_OK)
        else:
            total = total.iloc[0,0]
            my_data = my_data.fillna('')
            return Response({'data' :my_data.to_dict(orient='records'), 'total' : total , 'Page' : page , 'last_Page' : math.ceil( total / int(parPage) )  }, status=status.HTTP_200_OK , )        
        
    def get(self, request, id=None):
        if request.query_params:
            return self.searchActive(params=request.query_params)
        else:
            return  Response({"error" : "Provide for parameters for searching" , "error_ur" : "تلاش کے لیے پیرامیٹرز فراہم کریں۔"}  , status=status.HTTP_400_BAD_REQUEST ) 
