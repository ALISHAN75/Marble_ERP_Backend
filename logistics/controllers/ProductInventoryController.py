from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from accounts.CustomPermission import IsUserAllowed
from rest_framework import status
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


    def get(self, request):

        query = "SELECT left(O.ORDR_DT,7) Month_Name , sum(OI.REQ_QTY) Ordered_Qty , sum(OI.DLVRD_QTY) Delivered_Qty, sum(OI.REQ_QTY) + sum(OI.DLVRD_QTY) Total_Qty FROM  order_items OI join  orders O on OI.ORDR_ID = O.ORDR_ID and O.IS_ACTIVE = 1 group by left(O.ORDR_DT,7) order by Month_Name"
        my_data = pd.read_sql(query, connection)
        if my_data.empty:
            return Response({"error" : "No record found" , "error_ur" : "کوئی ریکارڈ نہیں ملا" }, status=400)
        else:
            return Response(my_data.to_dict('records'), status=200)

class ActiveInactiveOrdersListView(
    APIView,  # Basic View class provided by the Django Rest Framework
    UpdateModelMixin,  # Mixin that allows the basic APIView to handle PUT HTTP requests
    # Mixin that allows the basic APIView to handle DELETE HTTP request):
    DestroyModelMixin,
):


    def get(self, request):
        is_id_srch = 0
        ACCT_ID = request.query_params.get('ACCT_ID' , 0)
        DELVRY_STS = request.query_params.get('DELVRY_STS' , -1)
        ORDR_ID  = request.query_params.get('ORDR_ID' , 0)
        IS_SALE   = request.query_params.get('IS_SALE' , -1)
        if ORDR_ID == 0:
            is_id_srch = 1
        else:
            is_id_srch = 2
        try:
            query = """   
                    CALL `datafunc_Mabrle_ERP_wUrdu`.`LOGISTICS_Orders`(
                          """+str(is_id_srch)+""" -- Type_of_search ,  1: All based on given params
                        , """+str(ACCT_ID)+""" -- ACCT_ID
                        , """+str(DELVRY_STS)+""" -- DELVRY_STS
                        , """+str(ORDR_ID)+"""  -- Order_id
                        , """+str(IS_SALE)+"""  -- IS_SALE
                        );  """              
            my_data = pd.read_sql(query, connection)
        except ConnectionError:
            return Response({"error" : "Database Connection Error" , "error_ur" :  "ڈیٹا بیس کنکشن کی خرابی " }, status=status.HTTP_400_BAD_REQUEST)
        if my_data.empty:
            return Response([], status=status.HTTP_200_OK)
        else:
            my_data = my_data.fillna('')
            return Response(my_data.to_dict(orient='records'), status=status.HTTP_200_OK )        
