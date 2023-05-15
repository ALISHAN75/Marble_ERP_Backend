
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


class AcctLedgerListView(
    APIView,  # Basic View class provided by the Django Rest Framework
    UpdateModelMixin,  # Mixin that allows the basic APIView to handle PUT HTTP requests
    # Mixin that allows the basic APIView to handle DELETE HTTP request):
    DestroyModelMixin,
):
    permission_classes = [AllowAny]
    renderer_classes = [UserRenderer]
    rec_is_active = 1

    def getOne(self, request, id):
        if id:
            try:
                query = """ CALL `datafunc_Mabrle_ERP_wUrdu`.`ACCT_Ledger`(1 , """+str(id)+""", 0 , 1, 1); """     
                my_data = pd.read_sql(query, connection)
            except ConnectionError:
                return Response(  {"error" : "Database Connection Error" , "error_ur" :  "ڈیٹا بیس کنکشن کی خرابی " }  , status=status.HTTP_400_BAD_REQUEST)
        my_data = my_data.fillna('')
        if my_data.empty:
            return Response(  {"error" : "No record found" , "error_ur" : "کوئی ریکارڈ نہیں ملا" }  , status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(my_data.to_dict(orient='records')  , status=status.HTTP_200_OK)
             

    def getAll(self):
        try:
            query = """ CALL `datafunc_Mabrle_ERP_wUrdu`.`ACCT_Ledger`(2,0,0,1,1000000); """    
            my_data = pd.read_sql(query, connection)
        except ConnectionError:
            return Response({"error" : "Database Connection Error" , "error_ur" :  "ڈیٹا بیس کنکشن کی خرابی " }, status=status.HTTP_400_BAD_REQUEST)      
        my_data = my_data.fillna('')
        if my_data.empty:
            return Response(  {"error" : "No record found" , "error_ur" : "کوئی ریکارڈ نہیں ملا" }  , status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(my_data.to_dict(orient='records'), status=status.HTTP_200_OK)

    def searchActive(self, params):
        is_id_srch = 0
        page = int(params.get('page' , 1) ) 
        parPage = params.get('perPage' , 10)
        ACCT_ID = params.get('ACCT_ID' , 0) 
        q = params.get('q' , '') 
        if len(q)>0:
            is_id_srch = 3
            q = dateConversion(q)
        else:
            is_id_srch = 2
        try:
            query = """ CALL `datafunc_Mabrle_ERP_wUrdu`.`ACCT_Ledger`("""+str(is_id_srch)+""" , '"""+q+"""', """+str(ACCT_ID)+""" ,"""+str(page)+""" , """+str(parPage)+"""); """       
            my_data = pd.read_sql(query, connection)
            query = """ select FOUND_ROWS() """       
            total = pd.read_sql(query, connection)
        except ConnectionError:
                return Response({"error" : "Database Connection Error" , "error_ur" :  "ڈیٹا بیس کنکشن کی خرابی " }, status=status.HTTP_400_BAD_REQUEST)      
        if my_data.empty:
            return Response([], status=status.HTTP_200_OK)
        else:
            total = total.iloc[0,0]
            my_data = my_data.fillna('')
            return Response({'data' :my_data.to_dict(orient='records'), 'total' : total , 'Page' : page , 'last_Page' : math.ceil( total / int(parPage) )  }, status=status.HTTP_200_OK , )        
        
    def get(self, request, id=None):
        if id:
            return self.getOne(request, id)
        elif request.query_params:
            return self.searchActive(params=request.query_params)
        else:
            return self.getAll()


class LedgerByAcct(APIView):
    renderer_classes = [UserRenderer]
    # permission_classes = [IsAdminUser]

    def post(self, request , format=None):
        try:
            query = """ CALL `datafunc_Mabrle_ERP_wUrdu`.`ACCT_Ledger`(1 , """+str(request.data["ACC_ID"])+""", 0 , 1, 1); """     
            my_data = pd.read_sql(query, connection)
        except ConnectionError:
            return Response({"error" : "Database Connection Error" , "error_ur" :  "ڈیٹا بیس کنکشن کی خرابی " }, status=status.HTTP_400_BAD_REQUEST)

        my_data = my_data.fillna('')
        if my_data.empty:
            return Response(  {"error" : "No record found" , "error_ur" : "کوئی ریکارڈ نہیں ملا" } ,   status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(my_data.to_dict(orient='records')  , status=status.HTTP_200_OK)
