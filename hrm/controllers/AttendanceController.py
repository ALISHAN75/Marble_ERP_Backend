from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from django.http import JsonResponse
from accounts.CustomPermission import IsUserAllowed
from datetime import datetime
from accounts.renderers import UserRenderer
# util
import math
import pandas as pd
from django.db import connection
from inventory.utility.DataConversion import dateConversion
# models imports
from hrm.model.Employee_Attendance import Employee_Attendance
# serializers imports
from hrm.serializer.EmployeeAttendanceSerializer import EmployeeAttendanceSerializer


class EmployeeAttendanceListView(
    APIView,  # Basic View class provided by the Django Rest Framework
    UpdateModelMixin,  # Mixin that allows the basic APIView to handle PUT HTTP requests
    # Mixin that allows the basic APIView to handle DELETE HTTP request):
    DestroyModelMixin,
):
    permission_classes = [IsUserAllowed({'POST': 'hrm.add_employee_attendance', 'PUT': 'hrm.change_employee_attendance',
                                        'DELETE': 'hrm.delete_employee_attendance', 'GET': 'hrm.view_employee_attendance'})]
    renderer_classes = [UserRenderer]


    def getOne(self, request, id):
        if id:
            try:
                query = """  CALL `datafunc_Mabrle_ERP_wUrdu`.`HRM_Employee_Attendance`(
                            2   		     -- IS_ID_SRCH 2 = all , 3 =  query search 
                            , 'Shehroz'      -- srch query ( ALI )
                            , 1              -- page 
                            , 10             -- perPage 
                            , '2023-01-01'    -- Date  , '2023-01-01'
                            , """+str(id)+"""  -- 0 = ID  , INT given ID 
                            ); """  

                employee = pd.read_sql(query, connection)
            except ConnectionError:
                return Response({"error" : "Database Connection Error" , "error_ur" :  "ڈیٹا بیس کنکشن کی خرابی " }, status=status.HTTP_400_BAD_REQUEST)
        if employee.empty:
            return Response({"error" : "No record found" , "error_ur" : "کوئی ریکارڈ نہیں ملا" }, status=status.HTTP_400_BAD_REQUEST)
        else:
            employee = employee.fillna('')
            employee_data=employee.to_dict(orient='records')[0]
            return Response(employee_data  , status=status.HTTP_200_OK)

             

    def getAll(self):
        year = datetime.now().strftime('%Y') 
        month = datetime.now().strftime('%m')
        date_str = year+'-'+month+'-'+'05' 
        try:
            query = """  CALL `datafunc_Mabrle_ERP_wUrdu`.`HRM_Employee_Attendance`(
                            2   		     -- IS_ID_SRCH 2 = all , 3 =  query search 
                            , 'Shehroz'      -- srch query ( ALI )
                            , 1              -- page 
                            , 10             -- perPage 
                            , '"""+date_str+"""'    -- Date  , '2023-01-01'
                            , 0               -- 0 = ID  , INT given ID 
                            ); """  

            my_data = pd.read_sql(query, connection)
        except ConnectionError:
            return Response({"error" : "Database Connection Error" , "error_ur" :  "ڈیٹا بیس کنکشن کی خرابی " }, status=status.HTTP_400_BAD_REQUEST)
        if my_data.empty:
            return Response({"error" : "No record found" , "error_ur" : "کوئی ریکارڈ نہیں ملا" }, status=status.HTTP_400_BAD_REQUEST)
        else:
            my_data = my_data.fillna('')
            return Response(my_data.to_dict(orient='records'), status=status.HTTP_200_OK)

    def searchActive(self, params):
        y = datetime.now().strftime('%Y') 
        m = datetime.now().strftime('%m')
        page = int(params.get('page' , 1) ) 
        parPage = params.get('perPage' , 10)
        employee_name  =   params.get('employee_name' , '') 
        month = params.get('month' , y)
        year = params.get('year' , m )
        date_str = year+'-'+month+'-'+'05'

        try:
            query = """  CALL `datafunc_Mabrle_ERP_wUrdu`.`HRM_Employee_Attendance`(
                            3   		     -- IS_ID_SRCH 2 = all , 3 =  query search 
                            , '"""+employee_name+"""'      -- srch query ( ALI )
                            , """+str(page)+"""              -- page 
                            , """+str(parPage)+"""             -- perPage 
                            ,'"""+date_str+"""'     -- Date  , '2023-01-01'
                            , 0               -- 0 = All , ID  , INT given ID 
                            ); """
            my_data = pd.read_sql(query, connection)
            query = """ select FOUND_ROWS() """       
            total = pd.read_sql(query, connection)
        except ConnectionError:
                return Response({"error" : "Database Connection Error" , "error_ur" :  "ڈیٹا بیس کنکشن کی خرابی " }, status=status.HTTP_400_BAD_REQUEST)
        if my_data.empty:
            return Response([], status=status.HTTP_200_OK)
        else:      
            total = total.iloc[0,0]
            my_data = my_data.fillna('')
            return Response({'data' :my_data.to_dict(orient='records'), 'total' : total , 'Page' : page , 'last_Page' : math.ceil( total / int(parPage) )  }, status=status.HTTP_200_OK  )        
        
    def get(self, request, id=None):
        if id:
            return self.getOne(request, id)
        elif request.query_params:
            return self.searchActive(params=request.query_params)
        else:
            return self.getAll()

    def post(self, request):
        request.data["REC_ADD_BY"] = request.user.id
        request.data["REC_MOD_BY"] = request.user.id

        create_serializer = EmployeeAttendanceSerializer(data=request.data)
        if create_serializer.is_valid():
            employee_attendance = create_serializer.save()
            # read_serializer = EmployeeAttendanceSerializer(employee_attendance)
            # return Response(read_serializer.data, status=201)
            return Response({'success' : "Data is saved successfully" ,  'success_ur' : "ڈیٹا کامیابی سے محفوظ ہو گیا ہے۔" } , status=status.HTTP_201_CREATED)
        return Response(create_serializer.errors, status=400)


