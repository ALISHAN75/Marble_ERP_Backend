from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from accounts.CustomPermission import IsUserAllowed
from accounts.renderers import UserRenderer
# util
import pandas as pd
from django.db import connection


class ProductInventoryListView(
    APIView,  # Basic View class provided by the Django Rest Framework
    UpdateModelMixin,  # Mixin that allows the basic APIView to handle PUT HTTP requests
    # Mixin that allows the basic APIView to handle DELETE HTTP request):
    DestroyModelMixin,
):
    # permission_classes = [IsUserAllowed({'POST': 'inventory.add_orders', 'PUT': 'inventory.change_orders', 'DELETE': 'inventory.delete_orders', 'GET': 'inventory.view_orders'})]
    # permission_classes = [AllowAny]
    # renderer_classes = [UserRenderer]

    def get(self, request):      
        query = """SELECT PN.PROD_NM lables ,PN.PROD_NM_UR lables_ur, sum(PI.AVLBL_SQFT) dataset From  products_inventory PI  
        join  products P on PI.PROD_ID = P.PRODUCT_ID join  product_name PN on P.PROD_NM_ID = PN.PROD_NM_ID 
        where PI.IS_AVLBL= 1 group by PN.PROD_NM order by dataset DESC limit 10"""
        my_data = pd.read_sql(query, connection)
        if my_data.empty:
            return Response( {"error" : "No record found" , "error_ur" : "کوئی ریکارڈ نہیں ملا" }, status=400)
        data = {'lables' : my_data['lables']}
        new_data = [
            {
             'data' : my_data['dataset'] ,
        } 
        ]
        
        data['datasets'] = new_data
        
        return Response(data, status=200)

