from django.db.models import Q
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework import filters
from rest_framework.permissions import AllowAny
from accounts.renderers import UserRenderer
# Utils
import pandas as pd
from django.db import connection




class InventoryTransactionSectioningGraphListView(
    APIView,  # Basic View class provided by the Django Rest Framework
    UpdateModelMixin,  # Mixin that allows the basic APIView to handle PUT HTTP requests
    # Mixin that allows the basic APIView to handle DELETE HTTP request):
    DestroyModelMixin,
):
    permission_classes = [AllowAny]
    rec_is_active = 1


    def searchActive(self, params):
        try:
            query = """ CALL `datafunc_Mabrle_ERP_wUrdu`.`Inventory_Transaction_Sectioning_graph`(1); """       
            balance  = pd.read_sql(query, connection)
        except ConnectionError:
                return Response({"error" : "Database Connection Error" , "error_ur" :  "ڈیٹا بیس کنکشن کی خرابی " }  , status=status.HTTP_400_BAD_REQUEST)         
        if balance.empty:
            return Response([], status=status.HTTP_200_OK)
        else:
            balance = balance.fillna(0)             
            dates = balance["YM"]
            LABOUR_SQFT = balance["LABOUR_SQFT"]
            ACCT_TITLE = balance["ACCT_TITLE"]
            ACCT_TITLE_UR = balance["ACCT_TITLE_UR"]

            # Create a pandas DataFrame from the lists
            df = pd.DataFrame({
                'dates': dates,
                'LABOUR_SQFT': LABOUR_SQFT,
                'ACCT_TITLE': ACCT_TITLE,
                'ACCT_TITLE_UR': ACCT_TITLE_UR
            })

            # Convert Amount column to numeric type
            df['LABOUR_SQFT'] = pd.to_numeric(df['LABOUR_SQFT'])

            # Group by dates and Product_names/Product_names_ur, and aggregate with sum
            df_grouped = df.groupby(['dates', 'ACCT_TITLE']).agg({'LABOUR_SQFT': 'sum'})
            df_grouped_ur = df.groupby(['dates', 'ACCT_TITLE_UR']).agg({'LABOUR_SQFT': 'sum'})

            # Pivot the table to have dates as rows and Product_names as columns
            df_pivot = df_grouped.pivot_table(index='dates', columns='ACCT_TITLE', values='LABOUR_SQFT').fillna(0)
            df_pivot_ur = df_grouped_ur.pivot_table(index='dates', columns='ACCT_TITLE_UR', values='LABOUR_SQFT').fillna(0)

            # Convert the pivot table to a list of dictionaries with the required structure
            result = {
                "TITLE": "Monthly credit earning",  
                "TITLE_UR": "مربع فٹ میں سیکشننگ کا کام",     
                "LABELS": list(df_pivot.index),
                "LABELS_UR": list(df_pivot.index),
                "DATASET": [],
                "DATASET_UR": []
            }

            for col in df_pivot.columns:
                result["DATASET"].append({
                    "label": col,
                    "data": list(df_pivot[col])
                })

            for col in df_pivot_ur.columns:
                result["DATASET_UR"].append({
                    "label": col,
                    "data": list(df_pivot_ur[col])
                })

            return Response(result, status=status.HTTP_200_OK )        
        
    def get(self, request, id=None):
        return self.searchActive(params=request.query_params)





