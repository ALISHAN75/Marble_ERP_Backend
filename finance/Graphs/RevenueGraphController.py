from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from accounts.CustomPermission import IsUserAllowed
from accounts.renderers import UserRenderer
# util
import pandas as pd
from django.db import connection


class RevenueGraphListView(
    APIView,  # Basic View class provided by the Django Rest Framework
    UpdateModelMixin,  # Mixin that allows the basic APIView to handle PUT HTTP requests
    # Mixin that allows the basic APIView to handle DELETE HTTP request):
    DestroyModelMixin,
):


    def get(self, request):    
        query = """SELECT A.ACCT_TITLE as labels , A.ACCT_TITLE_UR as labels_ur, sum(E.PYMNT_AMNT) dataset 
        FROM expense_transactions E 
        join accounts A on E.EXPNS_TYP_ACCT = A.ACCT_ID
        where A.ACCT_STS = 1 and E.IS_CASH = 1 and E.PAYMNT_DT 
        between DATE_SUB(current_date(), INTERVAL DAYOFMONTH( current_date() )-1 DAY) and current_date()
        """
        my_data = pd.read_sql(query, connection)
        if my_data.empty:
             return Response( {"error" : "No record found" , "error_ur" : "کوئی ریکارڈ نہیں ملا" }, status=400)
        else:
            return Response(my_data.to_dict('list'), status=200)
