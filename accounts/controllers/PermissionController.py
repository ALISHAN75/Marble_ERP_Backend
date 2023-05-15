from rest_framework import status
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework.response import Response
from accounts.renderers import UserRenderer
from rest_framework.permissions import IsAdminUser
from accounts.CustomPermission import IsUserAllowed
# models imports
from django.contrib.auth.models import Permission
# serializers imports
from accounts.serializer.PermissionsSerialzer import PermissionSerializer


class PermissionListView(
    APIView,  # Basic View class provided by the Django Rest Framework
    UpdateModelMixin,  # Mixin that allows the basic APIView to handle PUT HTTP requests
    # Mixin that allows the basic APIView to handle DELETE HTTP request):
    DestroyModelMixin,
):
    renderer_classes = [UserRenderer]
    permission_classes = [IsUserAllowed({'POST': 'auth.add_permission', 'PUT': 'auth.change_permission',
                                        'DELETE': 'auth.delete_permission', 'GET': 'auth.view_permission'})]

    def get(self, request, id=None):
        try:
            permissions_queryset = Permission.objects.all().order_by('id')
        except Permission.DoesNotExist:
            return Response(permission_serializer.data, status=status.HTTP_404_NOT_FOUND)
        permission_serializer = PermissionSerializer(
            permissions_queryset, many=True)
        return Response(permission_serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PermissionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_permission = serializer.save()
        # read_serializer = PermissionSerializer(new_permission)
        # return Response(read_serializer.data, status=status.HTTP_201_CREATED)
        return Response({'success' : "Data is saved successfully" ,  'success_ur' : "ڈیٹا کامیابی سے محفوظ ہو گیا ہے۔" } , status=status.HTTP_201_CREATED)

    def put(self, request, id=None):
        try:
            permission_to_update = Permission.objects.get(id=id)
        except Permission.DoesNotExist:
            return Response({"error" : "Permission does not exist" , "error_ur" : "اجازت موجود نہیں ہے۔"}  , status=status.HTTP_404_NOT_FOUND)
        update_serializer = PermissionSerializer(
            permission_to_update, data=request.data)
        update_serializer.is_valid(raise_exception=True)
        uodated_permission = update_serializer.save()

        # read_serializer = PermissionSerializer(uodated_permission)
        # return Response(read_serializer.data, status=status.HTTP_201_CREATED)
        return Response({'success' : "Data is saved successfully" ,  'success_ur' : "ڈیٹا کامیابی سے محفوظ ہو گیا ہے۔" } , status=status.HTTP_201_CREATED)

    def delete(self, request, id=None):
        try:
            permission_to_delete = Permission.objects.get(id=id)
        except Permission.DoesNotExist:
            return Response({"error" : "Permission does not exist" , "error_ur" : "اجازت موجود نہیں ہے۔"}  , status=status.HTTP_404_NOT_FOUND)

        permission_to_delete.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
