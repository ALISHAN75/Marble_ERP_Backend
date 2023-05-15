from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from accounts.CustomPermission import IsUserAllowed
from rest_framework import status
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
    # renderer_classes = [UserRenderer]

    def post(self, request):
        if request.data:
            start_date = request.data['start']
            end_date = request.data['end']
            query = """PN.PROD_NM lables,PN.PROD_NM_UR lables_ur, sum(DI.PROD_QTY) dataset FROM  deliveries D  join  
        delivery_items DI on D.DLVRY_ID = DI.DLVRY_ID join  products P on DI.PRODUCT_ID = P.PRODUCT_ID 
        join  product_name PN on P.PROD_NM_ID = PN.PROD_NM_ID 
        where D.IS_SALE = 1  and D.DLVRY_DT between '""" + start_date+"""' and '""" + end_date+"""' and 
        D.IS_ACTIVE = 1 and P.IS_ACTIVE = 1 and PN.IS_ACTIVE = 1  group by PN.PROD_NM 
        order by dataset DESC """

            my_data = pd.read_sql(query, connection)

            if my_data.empty:
                return Response({"error" : 'No data found in this range!'  , "error_ur" : "اس رینج میں کوئی ڈیٹا نہیں ملا" }, status=status.HTTP_400_BAD_REQUEST)
            data = {'lables': my_data['lables']}
            new_data = [
                {
                    'data': my_data['dataset']
                }
            ]

            data['datasets'] = new_data
            return Response(data, status=status.HTTP_200_OK)

        else:
            return Response( {"error" : "No record found" , "error_ur" : "کوئی ریکارڈ نہیں ملا" }, status=400)
