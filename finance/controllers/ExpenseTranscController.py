from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from accounts.CustomPermission import IsUserAllowed
from accounts.LedgerTransaction import LedgerTransaction
from accounts.renderers import UserRenderer
import math
from datetime import datetime
# models imports
from finance.model.Expense_Transactions import Expense_Transactions
from finance.serializer.EarningTranscSerializer import DetailedEarningTranscSerializer
# util
from inventory.utility.DataConversion import dateConversion
import pandas as pd
from django.db import connection
# serializers imports
from finance.serializer.ExpenseTransItemsSerializer import ExpenseTransItemsSerializer
from finance.serializer.ExpenseTransSerializer import DetailedExpenseTransSerializer, ExpenseTransSerializer ,AdvanceExpenseTransSerializer


class ExpenseTransListView(
    APIView,  # Basic View class provided by the Django Rest Framework
    UpdateModelMixin,  # Mixin that allows the basic APIView to handle PUT HTTP requests
    # Mixin that allows the basic APIView to handle DELETE HTTP request):
    DestroyModelMixin,
):
    permission_classes = [IsUserAllowed({'POST': 'finance.add_expense_transactions', 'PUT': 'finance.change_expense_transactions',
                                        'DELETE': 'finance.delete_expense_transactions', 'GET': 'finance.view_expense_transactions'})]
    renderer_classes = [UserRenderer]
    rec_is_active = 1
    
    
        
    def getOne(self, request, id):
        if id:
            try:
                query = """  CALL `datafunc_Mabrle_ERP_wUrdu`.`FIN_Expense`(1,"""+str(id)+""" , 0,0, '1969-01-01' , '2099-12-31' ,1,10 );"""    
                expns = pd.read_sql(query, connection)
                query = """  CALL `datafunc_Mabrle_ERP_wUrdu`.`FIN_Expense`(5,"""+str(id)+"""  , 0,0, '1969-01-01' , '2099-12-31' ,1,10 );"""    
                expns_items = pd.read_sql(query, connection)
            except ConnectionError:
                return Response({"error" : "Database Connection Error" , "error_ur" :  "ڈیٹا بیس کنکشن کی خرابی " }, status=status.HTTP_400_BAD_REQUEST)
        if expns.empty:
            return Response({"error" : "No record found" , "error_ur" : "کوئی ریکارڈ نہیں ملا" }, status=status.HTTP_400_BAD_REQUEST)
        else:
            expns = expns.fillna('')
            expns_data=expns.to_dict(orient='records')[0]
            expns_data['EXPNS_TRANS_ITEMS'] = expns_items.to_dict(orient='records')
            return Response(expns_data, status=status.HTTP_200_OK)
             

    def getAll(self):
        try:
            query = """  CALL `datafunc_Mabrle_ERP_wUrdu`.`FIN_Expense`(2,0, 0,0, '1969-01-01' , '2099-12-31' ,1,10000000 );"""    
            expns = pd.read_sql(query, connection)
        except ConnectionError:
            return Response({"error" : "Database Connection Error" , "error_ur" :  "ڈیٹا بیس کنکشن کی خرابی " }, status=status.HTTP_400_BAD_REQUEST)
        if expns.empty:
            return Response({"error" : "No record found" , "error_ur" : "کوئی ریکارڈ نہیں ملا" }, status=status.HTTP_400_BAD_REQUEST)
        else:
            expns = expns.fillna('')
            return Response(expns.to_dict(orient='records'), status=status.HTTP_200_OK)


    def searchActive(self, params):
        is_id_srch = 0
        page = int(params.get('page' , 1) ) 
        parPage = params.get('perPage' , 10)
        start_date = params.get('start_date' , '01/01/1969') 
        end_date = params.get('end_date'  ,    '31/12/2099') 
        srch_pay_to_acct_id = params.get('srch_pay_to_acct_id'  ,    0)
        srch_expns_typ_acct_id = params.get('srch_expns_typ_acct_id'  ,    0)
        q = params.get('q' , '') 
        start_date = dateConversion(start_date)
        end_date = dateConversion(end_date)
        if len(q)>0:
            is_id_srch = 3
            q = dateConversion(q)
        else:
            is_id_srch = 2
        try:
            query = """ CALL `datafunc_Mabrle_ERP_wUrdu`.`FIN_Expense`("""+str(is_id_srch)+"""  , '"""+q+"""', """+str(srch_pay_to_acct_id)+""", """+str(srch_expns_typ_acct_id)+""",  '"""+start_date+"""', '"""+end_date+"""'  , """+str(page)+""", """+str(parPage)+""" ); """       
            expns = pd.read_sql(query, connection)
            query = """ select FOUND_ROWS() """       
            total = pd.read_sql(query, connection)
        except ConnectionError:
            return Response({"error" : "Database Connection Error" , "error_ur" :  "ڈیٹا بیس کنکشن کی خرابی " }, status=status.HTTP_400_BAD_REQUEST)
        if expns.empty:
            return Response([], status=status.HTTP_200_OK)
        else:
            total = total.iloc[0,0]
            expns = expns.fillna('')
            return Response({'data' : expns.to_dict(orient='records'), 'total' : total , 'Page' : page , 'last_Page' : math.ceil( total / int(parPage) )  }, status=status.HTTP_200_OK , )        
        
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
            request.data["TOTAL_wTAX"] = request.data["TOTAL_noTAX"] * (1 + request.data["TAX_PRCNT"])
           
            if 'EXPNS_TRANS_ITEMS' in request.data and len(request.data["EXPNS_TRANS_ITEMS"])>0:
                create_serializer = ExpenseTransSerializer(data=request.data)
                if create_serializer.is_valid():
                    new_expense_transc = create_serializer.save()
                    # if 'EXPNS_TRANS_ITEMS' in request.data:
                    for EXPNS_ITEM in request.data["EXPNS_TRANS_ITEMS"]:
                            EXPNS_ITEM["EXPNS_TRANS_ID"] = new_expense_transc.EXPNS_TRANS_ID
                            EXPNS_ITEM["REC_ADD_BY"] = request.user.id
                            EXPNS_ITEM["ITEM_TOTAL"] = EXPNS_ITEM["ITEM_RATE_UNIT"] * EXPNS_ITEM["ITEM_UNIT_QUANTITY"]
                            create_item_serializer = ExpenseTransItemsSerializer(
                                data=EXPNS_ITEM)
                            if create_item_serializer.is_valid():
                                create_item_serializer.save()
                            else:
                                return Response(create_item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    

                    # read_serializer = DetailedExpenseTransSerializer(
                    #     new_expense_transc)
                    # return Response(read_serializer.data, status=status.HTTP_201_CREATED)
                    return Response({'success' : "Data is saved successfully" ,  'success_ur' : "ڈیٹا کامیابی سے محفوظ ہو گیا ہے۔" } , status=status.HTTP_201_CREATED)
                return Response(create_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                create_serializer = AdvanceExpenseTransSerializer(data=request.data)
                if create_serializer.is_valid():
                    new_expense_transc = create_serializer.save()
                    
                    # read_serializer = DetailedExpenseTransSerializer(
                    #     new_expense_transc)
                    # return Response(read_serializer.data, status=status.HTTP_201_CREATED)
                    return Response({'success' : "Data is saved successfully" ,  'success_ur' : "ڈیٹا کامیابی سے محفوظ ہو گیا ہے۔" } , status=status.HTTP_201_CREATED)
                return Response(create_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        create_serializer = ExpenseTransSerializer(data=request.data)
        if create_serializer.is_valid():
            new_earning_transc = create_serializer.save()
            return Response({'success' : "Data is saved successfully" ,  'success_ur' : "ڈیٹا کامیابی سے محفوظ ہو گیا ہے۔" } , status=status.HTTP_201_CREATED)
            # read_serializer = DetailedExpenseTransSerializer(new_earning_transc)
            # return Response(read_serializer.data, status=status.HTTP_201_CREATED)
        return Response(create_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


            
