from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAdminUser
from accounts.renderers import UserRenderer
# models imports
from hrm.model.Employment_Types import Employment_Types
# serializers imports
from hrm.serializer.EmploymentTypeSerializer import EmploymentTypeSerializer


class EmployeeTypeListView(
    APIView,  # Basic View class provided by the Django Rest Framework
    UpdateModelMixin,  # Mixin that allows the basic APIView to handle PUT HTTP requests
    # Mixin that allows the basic APIView to handle DELETE HTTP request):
    DestroyModelMixin,
):
    permission_classes = [IsAdminUser]
    renderer_classes = [UserRenderer]
    rec_is_active = 1

    def get(self, request, id=None):
        if id:
            try:
                queryset = Employment_Types.objects.get(EMP_TYP_ID=id)
            except Employment_Types.DoesNotExist:
                return Response({'error': 'The Designation does not exist.'  , "error_ur" : "عہدہ موجود نہیں ہے۔"  }, status=400)
            read_serializer = EmploymentTypeSerializer(queryset)
        else:
            queryset = Employment_Types.objects.all()
            read_serializer = EmploymentTypeSerializer(queryset, many=True)
        return Response(read_serializer.data, status=200)

    def post(self, request):
        request.data["REC_ADD_BY"] = request.user.id
        request.data["REC_MOD_BY"] = request.user.id

        create_serializer = EmploymentTypeSerializer(data=request.data)
        if create_serializer.is_valid():
            new_emp_type = create_serializer.save()
            # read_serializer = EmploymentTypeSerializer(new_emp_type)
            # return Response(read_serializer.data, status=201)
            return Response({'success' : "Data is saved successfully" ,  'success_ur' : "ڈیٹا کامیابی سے محفوظ ہو گیا ہے۔" } , status=201)

        return Response(create_serializer.errors, status=400)

    def put(self, request, id=None):
        try:
            desig_to_update = Employment_Types.objects.get(EMP_TYP_ID=id)
        except Employment_Types.DoesNotExist:
            return Response({'error': 'The Employment Type does not exist.'    , "error_ur" : "روزگار کی قسم موجود نہیں ہے۔"   }, status=400)

        request.data["REC_ADD_BY"] = desig_to_update.REC_ADD_BY
        request.data["REC_MOD_BY"] = request.user.id

        update_serializer = EmploymentTypeSerializer(
            desig_to_update, data=request.data)
        if update_serializer.is_valid():
            updated_type = update_serializer.save()
            # read_serializer = EmploymentTypeSerializer(updated_type)
            # return Response(read_serializer.data, status=200)
            return Response({'success' : "Data is saved successfully" ,  'success_ur' : "ڈیٹا کامیابی سے محفوظ ہو گیا ہے۔" } , status=200)
        return Response(update_serializer.errors, status=400)

    def delete(self, request, id=None):
        try:
            desig_to_delete = Employment_Types.objects.get(EMP_TYP_ID=id)
        except Employment_Types.DoesNotExist:
             return Response({'error': 'The Employment Type does not exist.'    , "error_ur" : "روزگار کی قسم موجود نہیں ہے۔"   }, status=400)

        desig_to_delete.REC_MOD_BY = request.user.id
        desig_to_delete.IS_ACTIVE = 0
        desig_to_delete.save()

        return Response(None, status=204)
