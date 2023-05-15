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




class PayableExpenseBalanceGraphListView(
    APIView,  # Basic View class provided by the Django Rest Framework
    UpdateModelMixin,  # Mixin that allows the basic APIView to handle PUT HTTP requests
    # Mixin that allows the basic APIView to handle DELETE HTTP request):
    DestroyModelMixin,
):
    permission_classes = [AllowAny]
    rec_is_active = 1


    def searchActive(self, params):
        try:
            query = """ CALL `datafunc_Mabrle_ERP_wUrdu`.`Payable_Expense_balance_Graph`(1); """       
            payblebalance  = pd.read_sql(query, connection)
        except ConnectionError:
                return Response({"error" : "Database Connection Error" , "error_ur" :  "ڈیٹا بیس کنکشن کی خرابی " }  , status=status.HTTP_400_BAD_REQUEST)         
        if payblebalance.empty:
            return Response([], status=status.HTTP_200_OK)
        else:
            payblebalance = payblebalance.fillna(0)             
            dates = payblebalance["YM"]
            Amount = payblebalance["AMOUNT"]
            Product_names = payblebalance["ACCT_TITLE"]
            Product_names_ur = payblebalance["ACCT_TITLE_UR"]

            # Create a pandas DataFrame from the lists
            df = pd.DataFrame({
                'dates': dates,
                'Amount': Amount,
                'Product_names': Product_names,
                'Product_names_ur': Product_names_ur
            })

            # Convert Amount column to numeric type
            df['Amount'] = pd.to_numeric(df['Amount'])

            # Group by dates and Product_names/Product_names_ur, and aggregate with sum
            df_grouped = df.groupby(['dates', 'Product_names']).agg({'Amount': 'sum'})
            df_grouped_ur = df.groupby(['dates', 'Product_names_ur']).agg({'Amount': 'sum'})

            # Pivot the table to have dates as rows and Product_names as columns
            df_pivot = df_grouped.pivot_table(index='dates', columns='Product_names', values='Amount').fillna(0)
            df_pivot_ur = df_grouped_ur.pivot_table(index='dates', columns='Product_names_ur', values='Amount').fillna(0)

            # Convert the pivot table to a list of dictionaries with the required structure
            result = {
                "TITLE": "Monthly credit expense",  
                "TITLE_UR": "ماہانہ کریڈٹ خرچہ",     
                "SUB_TITLE": "",     
                "SUB_TITLE_UR": "", 
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





