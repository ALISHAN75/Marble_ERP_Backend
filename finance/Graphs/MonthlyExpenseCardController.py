from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from accounts.CustomPermission import IsUserAllowed
from accounts.renderers import UserRenderer
# util
import pandas as pd
from django.db import connection


class ExpenseCardhListView(
    APIView,  # Basic View class provided by the Django Rest Framework
    UpdateModelMixin,  # Mixin that allows the basic APIView to handle PUT HTTP requests
    # Mixin that allows the basic APIView to handle DELETE HTTP request):
    DestroyModelMixin,
):


    def get(self, request):    
        query = """SELECT A.ACCT_TITLE as labels, A.ACCT_TITLE_UR as label_ur, sum(E.PYMNT_AMNT) dataset 
            FROM expense_transactions E 
            join accounts A on E.EXPNS_TYP_ACCT = A.ACCT_ID
            where A.IS_ACTIVE = 1 and E.IS_CASH = 1 
                and year(E.PAYMNT_DT) =  year(current_date) 
                and month(E.PAYMNT_DT) =  month(current_date)
                group by A.ACCT_TITLE_UR , A.ACCT_TITLE """
        my_data = pd.read_sql(query, connection)
        if my_data.empty:
             return Response( {"error" : "No record found" , "error_ur" : "کوئی ریکارڈ نہیں ملا" }, status=400)
        else:
            return Response(my_data.to_dict('list'), status=200)
