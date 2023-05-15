from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from accounts.CustomPermission import IsUserAllowed
from accounts.renderers import UserRenderer
# util
import pandas as pd
from django.db import connection


class ExpenseGraphListView(
    APIView,  # Basic View class provided by the Django Rest Framework
    UpdateModelMixin,  # Mixin that allows the basic APIView to handle PUT HTTP requests
    # Mixin that allows the basic APIView to handle DELETE HTTP request):
    DestroyModelMixin,
):
    

    def post(self, request):
        if request.data:
            start_date = request.data['start']
            end_date = request.data['end']
            query = """  SELECT A.ACCT_TITLE as labels , A.ACCT_TITLE_UR as labels_ur, sum(E.PYMNT_AMNT) dataset 
            FROM expense_transactions E 
            join accounts A on E.EXPNS_TYP_ACCT = A.ACCT_ID
            where A.IS_ACTIVE = 1 
            and E.PAYMNT_DT between '""" + start_date+"""' and '""" + end_date+"""'
            group by A.ACCT_TITLE , A.ACCT_TITLE_UR """


            my_data = pd.read_sql(query, connection)
            if my_data.empty:
                return Response( {"error" : "No record found" , "error_ur" : "کوئی ریکارڈ نہیں ملا" }, status=400)
            else:
                return Response(my_data.to_dict('list'), status=200)
        else:
            return Response( {"error" : "Please provide start date and end date" , "error_ur" : "براہ کرم شروع کی تاریخ اور اختتامی تاریخ فراہم کریں۔" } ,status=400)
