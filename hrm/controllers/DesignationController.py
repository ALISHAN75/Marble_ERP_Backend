from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from accounts.CustomPermission import IsUserAllowed
from accounts.renderers import UserRenderer
# models imports
from hrm.model.Employee_Designations import Employee_Designations
from hrm.model.Employee import Employee
# serializers imports
from hrm.serializer.DesignationSerializer import DesignationSerializer
# util
import math
import pandas as pd
from django.db import connection
from inventory.utility.DataConversion import dateConversion


class DesignationsListView(
    APIView,  # Basic View class provided by the Django Rest Framework
    UpdateModelMixin,  # Mixin that allows the basic APIView to handle PUT HTTP requests
    # Mixin that allows the basic APIView to handle DELETE HTTP request):
    DestroyModelMixin,
):
    permission_classes = [IsUserAllowed({'POST': 'hrm.add_employee_designations', 'PUT': 'hrm.change_employee_designations',
                                        'DELETE': 'hrm.delete_employee_designations', 'GET': 'hrm.view_employee_designations'})]
    renderer_classes = [UserRenderer]
    rec_is_active = 1



    def getOne(self, request, id):
        if id:
            try:
                query = """ CALL `datafunc_Mabrle_ERP_wUrdu`.`HRM_Designation`(1 , """+str(id)+""", 0 , 0 ); """     
                employee = pd.read_sql(query, connection)
            except ConnectionError:
                return Response({"error" : "Database Connection Error" , "error_ur" :  "ڈیٹا بیس کنکشن کی خرابی " }, status=status.HTTP_400_BAD_REQUEST)

        if employee.empty:
            return Response({"error" : "No record found" , "error_ur" : "کوئی ریکارڈ نہیں ملا" }, status=status.HTTP_200_OK)
        else:
            employee = employee.fillna('')
            employee_data=employee.to_dict(orient='records')[0]
            return Response(employee_data  , status=status.HTTP_200_OK)

             

    def getAll(self):
        try:
            query = """ CALL `datafunc_Mabrle_ERP_wUrdu`.`HRM_Designation`(2, 1, 1, 1000000 ); """    
            my_data = pd.read_sql(query, connection)
        except ConnectionError:
            return Response({"error" : "Database Connection Error" , "error_ur" :  "ڈیٹا بیس کنکشن کی خرابی " }, status=status.HTTP_400_BAD_REQUEST)

        if my_data.empty:
            return Response({"error" : "No record found" , "error_ur" : "کوئی ریکارڈ نہیں ملا" }, status=status.HTTP_400_BAD_REQUEST)
        else:
            my_data = my_data.fillna('')
            return Response(my_data.to_dict(orient='records'), status=status.HTTP_200_OK)

    def searchActive(self, params):
        page = int(params.get('page' , 1) ) 
        parPage = params.get('perPage' , 10)
        q = params.get('q' , '') 
        if len(q)>0:
            is_id_srch = 3
            q = dateConversion(q)
        else:
            is_id_srch = 2
        try:
            query = """ CALL `datafunc_Mabrle_ERP_wUrdu`.`HRM_Designation`("""+str(is_id_srch)+""" , '"""+q+"""', """+str(page)+""", """+str(parPage)+""" ); """       
            my_data = pd.read_sql(query, connection)
            query = """ select FOUND_ROWS() """       
            total = pd.read_sql(query, connection)

        except ConnectionError:
                return Response({"error" : "Database Connection Error" , "error_ur" :  "ڈیٹا بیس کنکشن کی خرابی " }, status=status.HTTP_400_BAD_REQUEST)

        if my_data.empty:
            return Response([], status=status.HTTP_400_BAD_REQUEST)
            # return Response({"error" : "No record found" , "error_ur" : "کوئی ریکارڈ نہیں ملا" }, status=status.HTTP_400_BAD_REQUEST)
        else:
            total = total.iloc[0,0]
            my_data = my_data.fillna('')
            return Response({'data' :my_data.to_dict(orient='records'), 'total' : total , 'Page' : page , 'last_Page' : math.ceil( total / int(parPage) )  }, status=status.HTTP_200_OK , )        

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

        create_serializer = DesignationSerializer(data=request.data)
        if create_serializer.is_valid():
            new_designation = create_serializer.save()
            # read_serializer = DesignationSerializer(new_designation)
            # return Response(read_serializer.data, status=201)
            return Response({'success' : "Data is saved successfully" ,  'success_ur' : "ڈیٹا کامیابی سے محفوظ ہو گیا ہے۔" } , status=status.HTTP_201_CREATED)
        return Response(create_serializer.errors, status=400)

    def put(self, request, id=None):
        try:
            desig_to_update = Employee_Designations.objects.get(
                EMP_DESIG_ID=id)
        except Employee_Designations.DoesNotExist:
            return Response({'error': 'The Designation does not exist.'  , "error_ur" : "عہدہ موجود نہیں ہے۔"  }, status=400)
        request.data["REC_ADD_BY"] = desig_to_update.REC_ADD_BY
        request.data["REC_MOD_BY"] = request.user.id
        update_serializer = DesignationSerializer(
            desig_to_update, data=request.data)
        if update_serializer.is_valid():
            updated_designation = update_serializer.save()
            # read_serializer = DesignationSerializer(updated_designation)
            # return Response(read_serializer.data, status=200)
            return Response({'success' : "Designation Updated Successfully" ,  'success_ur' : "عہدہ کامیابی کے ساتھ اپ ڈیٹ ہو گیاہے" } , status=status.HTTP_200_OK)
        return Response(update_serializer.errors, status=400)

    def delete(self, request, id=None):
        try:
            queryset = Employee.objects.filter(EMP_DESIG_ID=id, IS_ACTIVE=self.rec_is_active)
            if queryset:
                return Response({'error': 'It cannot be delete due to associated employee.'   , "error_ur" : "متعلقہ ملازم کی وجہ سے اسے حذف نہیں کیا جا سکتا۔"  }, status=200)
            desig_to_delete = Employee_Designations.objects.get(EMP_DESIG_ID=id)
        except Employee_Designations.DoesNotExist:
            return Response({'error': 'The Designation does not exist.'  , "error_ur" : "عہدہ موجود نہیں ہے۔"}, status=400)
        desig_to_delete.REC_MOD_BY = request.user.id
        desig_to_delete.IS_ACTIVE = 0
        desig_to_delete.save()

        return Response({'success' : "Designation is deleted successfully" ,  'success_ur' : "عہدہ کو کامیابی سے حذف کر دیا گیا ہے" } , status=status.HTTP_200_OK)
