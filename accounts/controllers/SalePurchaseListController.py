from django.db.models import Q
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework.decorators import action, permission_classes
from accounts.CustomPermission import IsUserAllowed
from accounts.renderers import UserRenderer
# utility
from inventory.utility.DataConversion import acctTypeParams
import pandas as pd
from django.db import connection
import math
import json
from inventory.utility.DataConversion import dateConversion
# models imports
from accounts.model.Account import Accounts
# serializers imports
from accounts.serializer.UsersSerializer import AddAccountsSerializer, AccountsDetailExtraSerializer, AccountsDetailSerializer,UserDetailSerializer,AccountsSerializer ,UserRegistrationSerializer , AddressSerializer


class SalesFactoryListView(
    APIView,  # Basic View class provided by the Django Rest Framework
    UpdateModelMixin,  # Mixin that allows the basic APIView to handle PUT HTTP requests
    # Mixin that allows the basic APIView to handle DELETE HTTP request):
    DestroyModelMixin,
):
    permission_classes = [IsUserAllowed({'POST': 'accounts.add_user', 'PUT': 'accounts.change_user',
                                        'DELETE': 'accounts.delete_user', 'GET': 'accounts.view_user'})]  
    # renderer_classes = [UserRenderer]


    def searchActive(self, params):
        if 'page' in params and  'perPage' in params and 'q' in params and 'ACCT_TYP' in params:
            page = int(params.get('page' , 1) ) 
            parPage = params.get('perPage' , 10)
            q = params.get('q')
            q = dateConversion(q) 
            try:
                Json_params = json.loads(params["ACCT_TYP"])
                l = len(Json_params)
                query = """CALL `datafunc_Mabrle_ERP_wUrdu`.`ACCT_Search`
                    ({0},'{1}','{2}','{3}','{4}','{5}','{6}','{7}' , '{8}',{9},{10} );""".format(Json_params[0],
                    Json_params[1%l],Json_params[2%l],Json_params[3%l],Json_params[4%l],
                    Json_params[5%l],Json_params[6%l],Json_params[7%l], q , page , parPage ) 
                my_data = pd.read_sql(query, connection)  
                query = """ select FOUND_ROWS() """       
                total = pd.read_sql(query, connection)
            except ConnectionError:
                return Response( {"error" : "Database Connection Error" , "error_ur" :  "ڈیٹا بیس کنکشن کی خرابی " }  , status=status.HTTP_400_BAD_REQUEST)           
            if my_data.empty:
                return Response([], status=status.HTTP_200_OK)
            else:
                total = total.iloc[0,0]
                my_data = my_data.fillna('')
                return Response({'data' :my_data.to_dict(orient='records'), 'total' : total , 'Page' : page , 'last_Page' : math.ceil( total / int(parPage) )  }, status=status.HTTP_200_OK , )        
 
        if 'page' not in  params and 'ACCT_TYP' in params:
            Json_params = json.loads(params["ACCT_TYP"])
            l = len(Json_params)
            try:
                query = """CALL `datafunc_Mabrle_ERP_wUrdu`.`Account_List`
                    ({0},'{1}','{2}','{3}','{4}','{5}','{6}','{7}');""".format(Json_params[0],
                    Json_params[1%l],Json_params[2%l],Json_params[3%l],Json_params[4%l],
                    Json_params[5%l],Json_params[6%l],Json_params[7%l])    
                my_data = pd.read_sql(query, connection)  
            except ConnectionError:
                return Response({"error" : "Database Connection Error" , "error_ur" :  "ڈیٹا بیس کنکشن کی خرابی " }  , status=status.HTTP_400_BAD_REQUEST)               
            if my_data.empty:
                return Response([], status=status.HTTP_200_OK)
            else:
                my_data = my_data.fillna('')
                return Response( my_data.to_dict(orient='records') , status=status.HTTP_200_OK  )    
        
    def get(self, request, id=None):
        if id:
            return self.getOne(request, id)
        elif request.query_params:
            return self.searchActive(params=request.query_params)
        else:
            return self.getAll()
