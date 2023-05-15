from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from accounts.CustomPermission import IsUserAllowed
from accounts.LedgerTransaction import LedgerTransaction
from accounts.renderers import UserRenderer
# models imports
from finance.model.Earning_Transactions import Earning_Transactions
# util
import pandas as pd
from django.db import connection
from inventory.utility.DataConversion import dateConversion
# serializers imports
from finance.serializer.EarningTransItemsSerializer import EarningTransItemsSerializer
from finance.serializer.EarningTranscSerializer import DetailedEarningTranscSerializer,EarningTranscSerializer , AdvanceEarningTranscSerializer , SecondEarningTranscSerializer , SecondAdvanceEarningTranscSerializer
import math
from datetime import datetime

class EarningTransListView(
    APIView,  # Basic View class provided by the Django Rest Framework
    UpdateModelMixin,  # Mixin that allows the basic APIView to handle PUT HTTP requests
    # Mixin that allows the basic APIView to handle DELETE HTTP request):
    DestroyModelMixin,
):
    permission_classes = [IsUserAllowed({'POST': 'finance.add_earning_transactions', 'PUT': 'finance.change_earning_transactions',
                                        'DELETE': 'finance.delete_earning_transactions', 'GET': 'finance.view_earning_transactions'})]
    renderer_classes = [UserRenderer]
    rec_is_active = 1



    def getOne(self, request, id):
        if id:
            try:
                query = """  CALL `datafunc_Mabrle_ERP_wUrdu`.`FIN_Earning`(1,"""+str(id)+""" , 0 , 2 , '1969-01-01' , '2099-12-31', 1 , 10 );"""    
                earn = pd.read_sql(query, connection)
                query = """  CALL `datafunc_Mabrle_ERP_wUrdu`.`FIN_Earning`(6,"""+str(id)+""" , 0 , 2 , '1969-01-01' , '2099-12-31',1,10 );"""    
                earn_items = pd.read_sql(query, connection)
            except ConnectionError:
                return Response({"error" : "Database Connection Error" , "error_ur" :  "ڈیٹا بیس کنکشن کی خرابی " } , status=status.HTTP_400_BAD_REQUEST)      

        if earn.empty:
            return Response({"error" : "No record found" , "error_ur" : "کوئی ریکارڈ نہیں ملا" }, status=status.HTTP_400_BAD_REQUEST)
        else:
            earn = earn.fillna('')
            earn_data=earn.to_dict(orient='records')[0]
            earn_data['EARNS_TRANS_ITEMS'] = earn_items.to_dict(orient='records')
            return Response(earn_data, status=status.HTTP_200_OK)
             

    def getAll(self):
        try:
            query = """ CALL `datafunc_Mabrle_ERP_wUrdu`.`FIN_Earning`( 2 , 1 , 0 , 2 , '1969-01-01' , '2099-12-31',1,1000000 ); """    
            my_data = pd.read_sql(query, connection)
        except ConnectionError:
            return Response({"error" : "Database Connection Error" , "error_ur" :  "ڈیٹا بیس کنکشن کی خرابی " }, status=status.HTTP_400_BAD_REQUEST)
        if my_data.empty:
            return Response({"error" : "No record found" , "error_ur" : "کوئی ریکارڈ نہیں ملا" }, status=status.HTTP_400_BAD_REQUEST)
        else:
            my_data = my_data.fillna('')
            return Response(my_data.to_dict(orient='records'), status=status.HTTP_200_OK)

    def searchActive(self, params):
        is_id_srch = 0
        page = int(params.get('page' , 1) ) 
        parPage = params.get('perPage')
        start_date = params.get('start_date' , '01/01/1969') 
        end_date = params.get('end_date'  ,    '31/12/2099') 
        srch_earn_typ_acct = params.get('srch_earn_typ_acct' ,  0)
        IS_CASH = params.get('IS_CASH'  ,    2)
        q = params.get('q' , '') 
        start_date = dateConversion(start_date)
        end_date = dateConversion(end_date)
        if len(q)>0:
            is_id_srch = 3
            q = dateConversion(q)
        else:
            is_id_srch = 2
        try:
            query = """ CALL `datafunc_Mabrle_ERP_wUrdu`.`FIN_Earning`("""+str(is_id_srch)+""" , '"""+q+"""', """+str(srch_earn_typ_acct)+""", """+str(IS_CASH)+""",  '"""+start_date+"""', '"""+end_date+"""'  , """+str(page)+""", """+str(parPage)+""" ); """           
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
            return Response({'data' : my_data.to_dict(orient='records'), 'total' : total , 'Page' : page , 'last_Page' : math.ceil( total / int(parPage) )  }, status=status.HTTP_200_OK , )           

        
    def get(self, request, id=None):
        if id:
            return self.getOne(request, id)
        elif request.query_params:
            return self.searchActive(params=request.query_params)
        else:
            return self.getAll()


    def post(self, request):
        if request.data:
            request.data["REC_ADD_BY"] = request.user.id
            if 'EARNS_TRANS_ITEMS' in request.data and len(request.data["EARNS_TRANS_ITEMS"])>0:
                if request.data["IS_CASH"] == 1:
                    create_serializer = EarningTranscSerializer(data=request.data)
                if request.data["IS_CASH"] == 0:
                    create_serializer = SecondEarningTranscSerializer(data=request.data)
                if create_serializer.is_valid():
                    new_earning_transc = create_serializer.save()   
                    for EARNS_ITEM in request.data["EARNS_TRANS_ITEMS"]:
                            EARNS_ITEM["EARN_TRANS_ID"] = new_earning_transc.EARN_TRANS_ID
                            EARNS_ITEM["REC_ADD_BY"] = request.user.id
                            EARNS_ITEM["ITEM_TOTAL"] = EARNS_ITEM["ITEM_UNIT_AMNT"] * EARNS_ITEM["ITEM_UNIT_QUANTITY"]    
                            create_item_serializer = EarningTransItemsSerializer(data=EARNS_ITEM)
                            if create_item_serializer.is_valid():
                                create_item_serializer.save()
                            else:
                                return Response(create_item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    
                    # read_serializer = DetailedEarningTranscSerializer(
                    #     new_earning_transc)
                    # return Response(read_serializer.data, status=status.HTTP_201_CREATED)
                    return Response({'success' : "Data is saved successfully" ,  'success_ur' : "ڈیٹا کامیابی سے محفوظ ہو گیا ہے۔" } , status=status.HTTP_201_CREATED)
                return Response(create_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                if "IS_CASH" in request.data and  request.data["IS_CASH"] == 1:
                    create_serializer = AdvanceEarningTranscSerializer(data=request.data)
                if "IS_CASH" in request.data and  request.data["IS_CASH"] == 0:
                    create_serializer = SecondAdvanceEarningTranscSerializer(data=request.data)
                if create_serializer.is_valid():
                    new_earning_transc = create_serializer.save()  
                    
                    # read_serializer = DetailedEarningTranscSerializer(new_earning_transc)
                    # return Response(read_serializer.data, status=status.HTTP_201_CREATED)
                    return Response({'success' : "Data is saved successfully" ,  'success_ur' : "ڈیٹا کامیابی سے محفوظ ہو گیا ہے۔" } , status=status.HTTP_201_CREATED)
                return Response(create_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        create_serializer = EarningTranscSerializer(data=request.data)
        if create_serializer.is_valid():
            new_earning_transc = create_serializer.save()
            # read_serializer = DetailedEarningTranscSerializer(new_earning_transc)
            # return Response(read_serializer.data, status=status.HTTP_201_CREATED)
            return Response({'success' : "Data is saved successfully" ,  'success_ur' : "ڈیٹا کامیابی سے محفوظ ہو گیا ہے۔" } , status=status.HTTP_201_CREATED)
        return Response(create_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



        


