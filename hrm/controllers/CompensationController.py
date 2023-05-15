from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAdminUser
from accounts.renderers import UserRenderer
# models imports
from hrm.model.Employee import Employee_Compensation
# serializers imports
from hrm.serializer.EmployeeCompensationSerializer import EmployeeCompensationSerializer


class EmployeeCompensationListView(
    APIView,  # Basic View class provided by the Django Rest Framework
    UpdateModelMixin,  # Mixin that allows the basic APIView to handle PUT HTTP requests
    # Mixin that allows the basic APIView to handle DELETE HTTP request):
    DestroyModelMixin,
):
    permission_classes = [IsAdminUser]
    renderer_classes = [UserRenderer]

    def get(self, request, id=None):
        if id:
            try:
                queryset = Employee_Compensation.objects.get(EMP_CMPNSTN_ID=id)
            except Employee_Compensation.DoesNotExist:
                return Response({'error': 'The Compensation does not exist.'  , "error_ur" : "معاوضہ موجود نہیں ہے۔"}, status=400)
            read_serializer = EmployeeCompensationSerializer(queryset)
        else:
            queryset = Employee_Compensation.objects.all()
            read_serializer = EmployeeCompensationSerializer(
                queryset, many=True)
        return Response(read_serializer.data, status=200)

    def post(self, request):
        request.data["REC_ADD_BY"] = request.user.id
        request.data["REC_MOD_BY"] = request.user.id

        create_serializer = EmployeeCompensationSerializer(data=request.data)
        if create_serializer.is_valid():
            emp_compensation = create_serializer.save()
            # read_serializer = EmployeeCompensationSerializer(emp_compensation)
            # return Response(read_serializer.data, status=201)
            return Response({'success' : "Data is saved successfully" ,  'success_ur' : "ڈیٹا کامیابی سے محفوظ ہو گیا ہے۔" } , status=201)
        return Response(create_serializer.errors, status=400)

    def put(self, request, id=None):
        try:
            cmpnstn_to_update = Employee_Compensation.objects.get(EMP_ID=id)
        except Employee_Compensation.DoesNotExist:
            return Response({'error': 'The Compensation does not exist.'  , "error_ur" : "معاوضہ موجود نہیں ہے۔"}, status=400)

        request.data["REC_ADD_BY"] = cmpnstn_to_update.REC_ADD_BY
        request.data["REC_MOD_BY"] = request.user.id

        update_serializer = EmployeeCompensationSerializer(
            cmpnstn_to_update, data=request.data)
        if update_serializer.is_valid():
            updated_cmpnstn = update_serializer.save()
            # read_serializer = EmployeeCompensationSerializer(updated_cmpnstn)
            # return Response(read_serializer.data, status=200)
            return Response({'success' : "Data is saved successfully" ,  'success_ur' : "ڈیٹا کامیابی سے محفوظ ہو گیا ہے۔" } , status=200)
        return Response(update_serializer.errors, status=400)

    def delete(self, request, id=None):
        try:
            emp_to_delete = Employee_Compensation.objects.get(EMP_ID=id)
        except Employee_Compensation.DoesNotExist:
            return Response({'error': 'The Compensation does not exist.'  , "error_ur" : "معاوضہ موجود نہیں ہے۔"}, status=400)

        emp_to_delete.REC_MOD_BY = request.user.id
        emp_to_delete.IS_ACTIVE = 0
        emp_to_delete.save()

        return Response(None, status=204)
