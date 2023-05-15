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




class EmployeeSalaryAttendeceGraphListView(
    APIView,  # Basic View class provided by the Django Rest Framework
    UpdateModelMixin,  # Mixin that allows the basic APIView to handle PUT HTTP requests
    # Mixin that allows the basic APIView to handle DELETE HTTP request):
    DestroyModelMixin,
):
    permission_classes = [AllowAny]
    rec_is_active = 1


    def searchActive(self, params):
        acct_id = params.get('acct_id' ,  0)
        try:
            query = """ CALL `datafunc_Mabrle_ERP_wUrdu`.`HRM_Employee_Summary_Graph`(1 , """+str(acct_id)+""" ); """     
            attendence = pd.read_sql(query, connection)
            query = """ CALL `datafunc_Mabrle_ERP_wUrdu`.`HRM_Employee_Summary_Graph`(2 , """+str(acct_id)+""" ); """     
            salary = pd.read_sql(query, connection)
        except ConnectionError:
                return Response({"error" : "Database Connection Error" , "error_ur" :  "ڈیٹا بیس کنکشن کی خرابی " }  , status=status.HTTP_400_BAD_REQUEST)         
        if attendence.empty and  salary.empty:
            return Response([], status=status.HTTP_200_OK)
        else:
            salary = salary.fillna(0)
            attendence = attendence.fillna(0)
                
            graph_data = {          
                "TITLE": "Employee Summary",       
                "TITLE_UR": "ملازم کا خلاصہ",     
                "LABELS": "",     
                "LABELS_UR": "",     
                "LABELS": attendence["YM"] ,    
                "LABELS_UR": attendence["YM"]   ,   
                 "DATASET": [         
                    {    "label": "Attendance",            "data": attendence["Attendence"] } ,
                    {    "label": "Salary",            "data": salary["Salary"] } 
                    
                     ] ,
                "DATASET": [         
                    {    "label": "حاضری",            "data": attendence["Attendence"] } ,
                    {    "label": "تنخواہ",            "data": salary["Salary"] } 
                    
                     ] 
            }

            return Response(graph_data, status=status.HTTP_200_OK )        
        
    def get(self, request, id=None):
        return self.searchActive(params=request.query_params)





