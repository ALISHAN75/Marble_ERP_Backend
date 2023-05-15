from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from accounts.CustomPermission import IsUserAllowed
from accounts.renderers import UserRenderer
# util
import pandas as pd
from django.db import connection
# Utils
from marble_erp.utils.langDetector import lang_detect
from marble_erp.utils.lang_translate import lang_translate


class OrderGraphListView(
    APIView,  # Basic View class provided by the Django Rest Framework
    UpdateModelMixin,  # Mixin that allows the basic APIView to handle PUT HTTP requests
    # Mixin that allows the basic APIView to handle DELETE HTTP request):
    DestroyModelMixin,
):
    # permission_classes = [IsUserAllowed({'POST': 'inventory.add_orders', 'PUT': 'inventory.change_orders', 'DELETE': 'inventory.delete_orders', 'GET': 'inventory.view_orders'})]
    # permission_classes = [AllowAny]
    # renderer_classes = [UserRenderer]

    def get(self, request):

        query = """SELECT left(O.ORDR_DT,7) lables , sum(OI.REQ_QTY) Ordered_Qty , 
                sum(OI.DLVRD_QTY) Delivered_Qty, sum(OI.REQ_QTY) + sum(OI.DLVRD_QTY) Total_Qty 
                FROM  order_items OI join orders O on OI.ORDR_ID = O.ORDR_ID and O.IS_ACTIVE = 1  and O.ORDR_DT >= DATE_SUB(CURDATE() - INTERVAL 6 MONTH, INTERVAL DAYOFMONTH(CURDATE() - INTERVAL 6 MONTH)-1 DAY) 
                group by left(O.ORDR_DT,7)  
                order by lables  """
        my_data = pd.read_sql(query, connection)
        if my_data.empty:
            return Response( {"error" : "No record found" , "error_ur" : "کوئی ریکارڈ نہیں ملا" }, status=400)
        data = {'lables' : my_data['lables']}
        new_data = [
            {
            'label': 'Ordered Quantity' , 'label_ur': "آرڈر کی مقدار" , 
             'data' : my_data['Ordered_Qty'] ,
        } , 
            {
            'label': 'Delivered Quantity' , 'label_ur': "ڈیلیور شدہ مقدار"  , 
             'data' : my_data['Delivered_Qty'] ,
        } , 
            {
            'label': 'Total Quantity' , 'label_ur': "کل مقدار" , 
             'data' : my_data['Total_Qty'] ,
        } , 
        
        ]

        
        data['datasets'] = new_data
        
        return Response(data, status=200)
