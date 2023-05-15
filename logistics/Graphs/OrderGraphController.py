from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from accounts.CustomPermission import IsUserAllowed
from accounts.renderers import UserRenderer
# util
import pandas as pd
from django.db import connection


class OrderGraphListView(
    APIView,  # Basic View class provided by the Django Rest Framework
    UpdateModelMixin,  # Mixin that allows the basic APIView to handle PUT HTTP requests
    # Mixin that allows the basic APIView to handle DELETE HTTP request):
    DestroyModelMixin,
):


    def get(self, request):

        # act_orders = Orders.objects.filter(IS_ACTIVE=1).annotate(month=TruncMonth('ORDR_DT')).values('month').annotate(total=Count('ORDR_ID'))
        query = "SELECT left(O.ORDR_DT,7) Month_Name , sum(OI.REQ_QTY) Ordered_Qty , sum(OI.DLVRD_QTY) Delivered_Qty, sum(OI.REQ_QTY) + sum(OI.DLVRD_QTY) Total_Qty FROM  order_items OI join  orders O on OI.ORDR_ID = O.ORDR_ID and O.IS_ACTIVE = 1 group by left(O.ORDR_DT,7) order by Month_Name"
        my_data = pd.read_sql(query, connection)
        if my_data.empty:
           return Response( {"error" : "No record found" , "error_ur" : "کوئی ریکارڈ نہیں ملا" }  , status=400)
        else:
            return Response(my_data.to_dict('records'), status=200)
