from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework import status
from accounts.renderers import UserRenderer
# util
import pandas as pd
from django.db import connection


class EmployeSalarywGraph(
    APIView,  # Basic View class provided by the Django Rest Framework
    UpdateModelMixin,  # Mixin that allows the basic APIView to handle PUT HTTP requests
    # Mixin that allows the basic APIView to handle DELETE HTTP request):
    DestroyModelMixin,
):
    # permission_classes = [IsUserAllowed({'POST': 'inventory.add_orders', 'PUT': 'inventory.change_orders', 'DELETE': 'inventory.delete_orders', 'GET': 'inventory.view_orders'})]
    # permission_classes = [AllowAny]
    # renderer_classes = [UserRenderer]

    def get(self, request):

        query = """ SELECT concat(u.FIRST_NAME, "  ", u.LAST_NAME) Full_Name, concat(u.FIRST_NAME_UR , "  " ,  u.LAST_NAME_UR) Full_Name_UR ,
        DATE_ADD(ET.PAYMNT_DT, INTERVAL -(case when (DAYOFWEEK(ET.PAYMNT_DT)-6)>= 0 
        then (DAYOFWEEK(ET.PAYMNT_DT)-6) else (DAYOFWEEK(ET.PAYMNT_DT)-6)+7 end) DAY) Week_Start_Date, 
        sum(ET.PYMNT_AMNT) Weekly_Expense
        FROM employees E
        join users u on E.USER_ID = u.ID
        join accounts a on u.ID = a.USER_ID
        join expense_transactions ET on ET.ACCT_ID = a.ACCT_ID
        join accounts A2 on ET.EXPNS_TYP_ACCT = A2.ACCT_ID
        where E.EMP_STS = 1 and E.IS_ACTIVE = 1 and A2.ACCT_TITLE = 'Salary'
        group by concat(u.FIRST_NAME, "  ", u.LAST_NAME) , concat(u.FIRST_NAME_UR , "  " ,  u.LAST_NAME_UR)  ,
        DATE_ADD(ET.PAYMNT_DT, INTERVAL -(case when (DAYOFWEEK(ET.PAYMNT_DT)-6)>= 0 
                    then (DAYOFWEEK(ET.PAYMNT_DT)-6) else (DAYOFWEEK(ET.PAYMNT_DT)-6)+7 end) DAY)
        order by Week_Start_Date;"""


        my_data = pd.read_sql(query, connection)
        if my_data.empty:
            return Response( {"error" : "No record found" , "error_ur" : "کوئی ریکارڈ نہیں ملا" }, status=400)
        full_data = {'lables' : my_data['Week_Start_Date']}
        data_dict = {}
        data_list = []

        # data_list = [
        #     {
        #     'label': 'Ordered_Qty' ,
        #      'data' : my_data['Ordered_Qty'] ,
        #    } , 
        #     {
        #     'label': 'Delivered_Qty' ,
        #      'data' : my_data['Delivered_Qty'] ,
        # } , 
        #     {
        #     'label': 'Total_Qty' ,
        #      'data' : my_data['Total_Qty'] ,
        # } ]
        
        for index, row in my_data.iterrows():
            data_dict = {
                'label': row["Full_Name"] ,
                'data' : [row['Weekly_Expense'] ] 
                }

            data_list.append(data_dict)
            


        full_data['datasets'] = data_list
        
        return Response(full_data, status=200)