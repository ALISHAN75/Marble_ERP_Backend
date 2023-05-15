from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from accounts.renderers import UserRenderer
import pandas as pd
from django.db import connection
# models
from django.contrib.auth.models import Group
from rest_framework.permissions import AllowAny
from accounts.CustomPermission import IsUserAllowed
#  serializers
from accounts.serializer.GroupSerializer import GroupListSerializer, GroupSerializer
from accounts.serializer.PermissionsSerialzer import PermissionSerializer
# Utils
from marble_erp.utils.langDetector import lang_detect
from marble_erp.utils.lang_translate import lang_translate




class UsersGroupCreateView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsUserAllowed({'POST': 'auth.add_group'})]

    def post(self, request, format=None):
        serializer = GroupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data         
        name = data.get("name")
        convertFrom, convertTo = lang_detect(name)
        name  , name_ur  = lang_translate(stringToConvert=name, from_lang=convertFrom, to_lang=convertTo)
        group = Group.objects.create(name=name , name_UR= name_ur)

        for permission in data.get('user_permissions'):
            permissionId = permission.get("id")
            permissionStatus = permission.get("status")
            if permissionStatus:
                group.permissions.add(permissionId)

        return   Response({"error" : "Role group created" , "error_ur" : "رول گروپ بنایا گیا۔"}  , status=status.HTTP_201_CREATED ) 


class GroupListView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        try:
            query = """ CALL `datafunc_Mabrle_ERP_wUrdu`.`ACCT_Roles`(1); """    
            my_data = pd.read_sql(query, connection)
            query = """ select FOUND_ROWS() """       
            total = pd.read_sql(query, connection)
        except ConnectionError:
            return Response({"error" : "Database Connection Error" , "error_ur" :  "ڈیٹا بیس کنکشن کی خرابی " }  , status=status.HTTP_400_BAD_REQUEST)

        if my_data.empty:
            return Response([], status=status.HTTP_200_OK)
        else:
            my_data = my_data.fillna('')
            total = len(my_data)
            return Response({'data' : my_data.to_dict(orient='records'), 'total' : total }, status=status.HTTP_200_OK , )        


class GroupPermissionsListView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsUserAllowed({'GET': 'auth.view_group'})]

    def get(self, request, id=None, format=None):
        try:
            grp_queryset = Group.objects.get(id=id)
        except Group.DoesNotExist:
            return Response({"error" : "Role group does not exist" , "error_ur" : "رول گروپ موجود نہیں ہے۔"}  , status=status.HTTP_404_NOT_FOUND)
        permissions_queryset = grp_queryset.permissions.all()
        permission_serializer = PermissionSerializer(
            permissions_queryset, many=True)

        return Response({
            "id": grp_queryset.id,
            "name": grp_queryset.name,
            "user_permissions": permission_serializer.data
        }, status=status.HTTP_200_OK)


class GroupPermissionsUpdateView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsUserAllowed({'PUT': 'auth.change_group'})]

    def put(self, request, id=None, format=None):
        try:
            group, created = Group.objects.get_or_create(id=id)
        except:
            return Response({"error" : "Role group does not exist" , "error_ur" : "رول گروپ موجود نہیں ہے۔"}  , status=status.HTTP_404_NOT_FOUND)
        update_serializer = GroupListSerializer(group, data=request.data)
        if update_serializer.is_valid(raise_exception=True):
            updated_department = update_serializer.save()
        for permission in request.data.get('user_permissions'):
            permissionId = permission.get("id")
            permissionStatus = permission.get("status")
            if permissionStatus:
                group.permissions.add(permissionId)
            else:
                group.permissions.remove(permissionId)

        return   Response({"error" : "Role group created" , "error_ur" : "رول گروپ بنایا گیا۔"}  , status=status.HTTP_201_CREATED ) 
