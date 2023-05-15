from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from accounts.CustomPermission import IsUserAllowed
from accounts.renderers import UserRenderer
# util
import pandas as pd
from django.db import connection


class SalesGraphListView(
    APIView,  # Basic View class provided by the Django Rest Framework
    UpdateModelMixin,  # Mixin that allows the basic APIView to handle PUT HTTP requests
    # Mixin that allows the basic APIView to handle DELETE HTTP request):
    DestroyModelMixin,
):
    permission_classes = [IsUserAllowed({'POST': 'inventory.add_orders', 'PUT': 'inventory.change_orders',
                                        'DELETE': 'inventory.delete_orders', 'GET': 'inventory.view_orders'})]

    def post(self, request):
        if request.data:
            start_date = request.data['start']
            end_date = request.data['end']
            query = "SELECT PN.PROD_NM, sum(DI.PROD_QTY) PROD_QTY FROM  DELIVERIES D  join  DELIVERY_ITEMS DI on D.DLVRY_ID = DI.DLVRY_ID join  products P on DI.PRODUCT_ID = P.PRODUCT_ID join  product_name PN on P.PROD_NM_ID = PN.PROD_NM_ID where D.IS_SALE = 1  and D.DLVRY_DT between '" + \
                start_date + "' and '" + end_date + \
                    "' and D.IS_ACTIVE = 1 and P.IS_ACTIVE = 1 and PN.IS_ACTIVE = 1  group by PN.PROD_NM order by PROD_QTY DESC"
            my_data = pd.read_sql(query, connection)

            if my_data.empty:
                return Response( {"error" : "No record found" , "error_ur" : "کوئی ریکارڈ نہیں ملا" }  , status=400)
            else:
                return Response(my_data.to_dict('records'), status=200)
