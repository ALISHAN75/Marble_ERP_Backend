from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from accounts.renderers import UserRenderer
from accounts.CustomPermission import IsUserAllowed
# util
import pandas as pd
from django.db import connection


class ExpenseGraphListView(
    APIView,  # Basic View class provided by the Django Rest Framework
    UpdateModelMixin,  # Mixin that allows the basic APIView to handle PUT HTTP requests
    # Mixin that allows the basic APIView to handle DELETE HTTP request):
    DestroyModelMixin,
):


    def get(self, request):
        query = "SELECT A.ACCT_TITLE, sum(E.PYMNT_AMNT) TOTAL_EXPENSE FROM  expense_transactions E join  accounts A on E.EXPNS_TYP_ACCT = A.ACCT_ID where A.ACCT_STS = 1 group by A.ACCT_TITLE;"
        my_data = pd.read_sql(query, connection)
        if my_data.empty:
            return Response( {"error" : "No record found" , "error_ur" : "کوئی ریکارڈ نہیں ملا" }  , status=400)
        else:
            return Response(my_data.to_dict('records'), status=200)
