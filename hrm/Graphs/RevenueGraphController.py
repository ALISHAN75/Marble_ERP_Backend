from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from accounts.renderers import UserRenderer
# util
import pandas as pd
from django.db import connection


class RevenueGraph(
    APIView,  # Basic View class provided by the Django Rest Framework
    UpdateModelMixin,  # Mixin that allows the basic APIView to handle PUT HTTP requests
    # Mixin that allows the basic APIView to handle DELETE HTTP request):
    DestroyModelMixin,
):
    # permission_classes = [IsUserAllowed({'POST': 'inventory.add_orders', 'PUT': 'inventory.change_orders', 'DELETE': 'inventory.delete_orders', 'GET': 'inventory.view_orders'})]
    # permission_classes = [AllowAny]
    # renderer_classes = [UserRenderer]

    def get(self, request):

        query = """SELECT sum( B.AVLBL_SQFT)/ sum(TD.QTY_SQFT )  * -1 as Breakage_Percent
            FROM transactions_details TD
            join inventory_transactions IT on IT.INV_TRANS_ID = TD.INV_TRANS_ID 
            and IT.TRANS_TYP in ( 'Polishing' , 'Sizing' , 'Gola' , 'Sectioning')
            left join breakage B on TD.INV_TRANS_ID = B.INV_TRANS_ID
            where TD.QTY_SQFT <0"""


        my_data = pd.read_sql(query, connection)
        if my_data.empty:
            return Response( {"error" : "No record found" , "error_ur" : "کوئی ریکارڈ نہیں ملا" }, status=400)
        else:
            return Response(my_data.to_dict('list'), status=200)
