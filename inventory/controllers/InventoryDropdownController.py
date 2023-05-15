from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from accounts.CustomPermission import IsUserAllowed
from rest_framework.permissions import AllowAny
from accounts.renderers import UserRenderer
import math
# util
import pandas as pd
from django.db import connection
from inventory.utility.DataConversion import dateConversion
# models imports
# serializers imports
from inventory.utility.AdjustmentUtil import isSectioned



class InventroyDropdownView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [AllowAny]
    

    def searchActive(self, params):
        Type_of_search = params.get('Type_of_search' , '') 
        q = params.get('q' , '') 
        PROD_NM_ID = params.get('PROD_NM_ID' , 0)
        CAT_ID = params.get('CAT_ID' , 0)
        USAGE_ID = params.get('USAGE_ID' , 0)
        IS_SIZED = params.get('IS_SIZED' , -1)
        IS_SECTIONED = params.get('IS_SECTIONED' , -1)
        IS_GOLA = params.get('IS_GOLA' , -1)
        IS_POLISHED = params.get('IS_POLISHED' , -1)
        WIDTH = params.get('WIDTH' , -1)
        LENGHT = params.get('LENGHT' , -1)
        THICKNESS = params.get('THICKNESS' , -1)      

        try:
            query = """ CALL `datafunc_Mabrle_ERP_wUrdu`.`Inventory_Product_Dropdown`(
                            '"""+str(Type_of_search)+"""' -- Type_of_search ,  "Inventory Products" or  "All Products"
                            , '"""+str(q)+"""' -- search query
                            , """+str(PROD_NM_ID)+"""  -- PROD_NM_ID
                            , """+str(CAT_ID)+""" -- CAT_ID
                            , """+str(USAGE_ID)+""" -- USAGE_ID
                            , """+str(IS_SIZED)+""" -- IS_SIZED
                            , """+str(IS_SECTIONED)+""" -- IS_SECTIONED
                            , """+str(IS_GOLA)+""" -- IS_GOLA
                            , """+str(IS_POLISHED)+""" -- IS_POLISHED
                            , """+str(WIDTH)+""" -- WIDTH
                            , """+str(LENGHT)+""" -- LENGHT
                            , """+str(THICKNESS)+""" -- THICKNESS
                            ); """ 


            my_data = pd.read_sql(query, connection)
            query = """ select FOUND_ROWS() """       
            total = pd.read_sql(query, connection)
        except ConnectionError:
                    return Response({"error" : "Database Connection Error" , "error_ur" :  "ڈیٹا بیس کنکشن کی خرابی " }, status=status.HTTP_400_BAD_REQUEST)       
        if my_data.empty:
            return Response([], status=status.HTTP_400_BAD_REQUEST)
        else:
            total = total.iloc[0,0]
            my_data = my_data.fillna('')
            return Response({'data' :my_data.to_dict(orient='records'), 'total' : total  }, status=status.HTTP_200_OK , )        
        
    def get(self, request, id=None):
        if request.query_params:
            return self.searchActive(params=request.query_params)
        else:
            return Response({"error" : "please provide search parameters"  ,  "error_ur" :  "براہ کرم تلاش کے پیرامیٹرز فراہم کریں۔" }, status=status.HTTP_200_OK , ) 
