from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from accounts.CustomPermission import IsUserAllowed
from accounts.renderers import UserRenderer

# util
import pandas as pd
from django.db import connection


class IncomeStatementList(
    APIView,  # Basic View class provided by the Django Rest Framework
    UpdateModelMixin,  # Mixin that allows the basic APIView to handle PUT HTTP requests
    # Mixin that allows the basic APIView to handle DELETE HTTP request):
    DestroyModelMixin,
):


    def post(self, request):
        if request.data:
            start_date = request.data['start']
            end_date = request.data['end']
        #     query = """  SELECT sum(E.PYMNT_AMNT) Sales_Income
        # FROM earning_transactions E
        # join accounts A on E.ACCT_ID = A.ACCT_ID and A.IS_ACTIVE = 1
        #     where E.PYMNT_DT between '""" + start_date+"""' and '""" + end_date+"""'; """


            query = """ CALL Income_Statement('""" + start_date+"""' , '""" + end_date+"""'); """

            my_data = pd.read_sql(query, connection)
            if my_data.empty:
                return Response( {"error" : "No record found" , "error_ur" : "کوئی ریکارڈ نہیں ملا" }, status=400)
            else:
                return Response(my_data.to_dict('list'), status=200)
        else:
            return Response( {"error" : "Please provide start date and end date" , "error_ur" : "براہ کرم شروع کی تاریخ اور اختتامی تاریخ فراہم کریں۔" } ,status=400)
