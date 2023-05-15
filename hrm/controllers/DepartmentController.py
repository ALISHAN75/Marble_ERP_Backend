from django.db.models import Q
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework import filters
from accounts.CustomPermission import IsUserAllowed
from accounts.renderers import UserRenderer
# models imports
from hrm.model.Employee_Departments import Employee_Departments
from hrm.model.Employee_Designations import Employee_Designations
# serializers imports
from hrm.serializer.DepartmentsSerializer import DepartmentsSerializer
# others
from rest_framework.decorators import api_view, action, permission_classes
from accounts.renderers import UserRenderer


class DepatmentsListView(
    APIView,  # Basic View class provided by the Django Rest Framework
    UpdateModelMixin,  # Mixin that allows the basic APIView to handle PUT HTTP requests
    # Mixin that allows the basic APIView to handle DELETE HTTP request):
    DestroyModelMixin,
):
    permission_classes = [IsUserAllowed({'POST': 'hrm.add_employee_departments', 'PUT': 'hrm.change_employee_departments',
                                        'DELETE': 'hrm.delete_employee_departments', 'GET': 'hrm.view_employee_departments'})]
    renderer_classes = [UserRenderer]
    rec_is_active = 1

    # @permission_classes([IsUserAllowed("hrm.view_employee_departments")])
    # @permission_classes((IsUserAllowed("hrm.view_employee_departments"),))
    def get(self, request, id=None):
        if id:
            try:
                queryset = Employee_Departments.objects.get(EMP_DEPT_ID=id)
            except Employee_Departments.DoesNotExist:
                return Response({'error': 'The Department does not exist.'  , "error_ur" : "محکمہ موجود نہیں ہے۔"}, status=400)
            read_serializer = DepartmentsSerializer(queryset)
        else:
            if request.query_params:
                params = request.query_params
                queryset = Employee_Departments.objects.filter(Q(DEPT_NM__icontains=params['search']) | Q(
                    DEPT_DESC__icontains=params['search']),  IS_ACTIVE=self.rec_is_active)
            else:
                queryset = Employee_Departments.objects.filter(
                    IS_ACTIVE=self.rec_is_active)
            read_serializer = DepartmentsSerializer(queryset, many=True)
        return Response(read_serializer.data, status=200)

    def post(self, request):
        request.data["REC_ADD_BY"] = request.user.id
        request.data["REC_MOD_BY"] = request.user.id

        create_serializer = DepartmentsSerializer(data=request.data)
        if create_serializer.is_valid():
            new_department = create_serializer.save()
            # read_serializer = DepartmentsSerializer(new_department)
            # return Response(read_serializer.data, status=201)
            return Response({'success' : "Data is saved successfully" ,  'success_ur' : "ڈیٹا کامیابی سے محفوظ ہو گیا ہے۔" } , status=201)
        return Response(create_serializer.errors, status=400)

    def put(self, request, id=None):
        try:
            dep_to_update = Employee_Departments.objects.get(EMP_DEPT_ID=id)
        except Employee_Departments.DoesNotExist:
            return Response({'error': 'The Department does not exist.'  , "error_ur" : "محکمہ موجود نہیں ہے۔"}, status=400)

        request.data["REC_ADD_BY"] = dep_to_update.REC_ADD_BY
        request.data["REC_MOD_BY"] = request.user.id

        update_serializer = DepartmentsSerializer(
            dep_to_update, data=request.data)
        if update_serializer.is_valid():
            updated_department = update_serializer.save()
            # read_serializer = DepartmentsSerializer(updated_department)
            # return Response(read_serializer.data, status=200)
            return Response({'success' : "Data is saved successfully" ,  'success_ur' : "ڈیٹا کامیابی سے محفوظ ہو گیا ہے۔" } , status=200)
        return Response(update_serializer.errors, status=400)

    def delete(self, request, id=None):
        try:
            queryset = Employee_Designations.objects.filter(
                EMP_DEPT_ID=id, IS_ACTIVE=self.rec_is_active) 
            if queryset:
                return Response({'error': 'It cannot be delete due to associated designation.' , "error_ur" : "متعلقہ عہدہ کی وجہ سے اسے حذف نہیں کیا جا سکتا"  }, status=200)
            dep_to_delete = Employee_Departments.objects.get(EMP_DEPT_ID=id)
        except Employee_Departments.DoesNotExist:
            return Response({'error': 'The Department does not exist.'  , "error_ur" : "محکمہ موجود نہیں ہے۔"  }, status=400)

        dep_to_delete.REC_MOD_BY = request.user.id
        dep_to_delete.IS_ACTIVE = 0
        dep_to_delete.save()

        return Response({'success' : "Department is deleted successfully" ,  'success_ur' : "ڈیپارٹمنٹ کو کامیابی سے حذف کر دیا گیا ہے" } , status=200)



