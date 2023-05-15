from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from accounts.CustomPermission import IsUserAllowed
from accounts.renderers import UserRenderer
# models imports
from inventory.model.UsageType import UsageType
# serializers imports
from inventory.serializers.UsageTypeSerializer import UsageTypeSerializer


class UsageTypeListView(
    APIView,  # Basic View class provided by the Django Rest Framework
    UpdateModelMixin,  # Mixin that allows the basic APIView to handle PUT HTTP requests
    # Mixin that allows the basic APIView to handle DELETE HTTP request):
    DestroyModelMixin,
):
    permission_classes = [IsUserAllowed({'POST': 'productusagetype.add_productusagetype', 'PUT': 'productusagetype.change_productusagetype',
                                        'DELETE': 'productusagetype.delete_productusagetype', 'GET': 'productusagetype.view_productusagetype'})]
    renderer_classes = [UserRenderer]
    ACTIVE_DEFAULT_VALUE = 1

    def get(self, request, id=None):
        if id:
            try:
                queryset = UsageType.objects.get(USAGE_ID=id)
            except UsageType.DoesNotExist:
                return Response({'error': 'The Product Usage Type does not exist.' , "error_ur" : "پروڈکٹ کے استعمال کی قسم موجود نہیں ہے۔" }, status=status.HTTP_400_BAD_REQUEST)
            read_serializer = UsageTypeSerializer(queryset)
        else:
            if request.query_params:
                params = request.query_params
                queryset = UsageType.objects.filter(Q(USAGE_NM__icontains=params['search']) | Q(
                    USAGE_DESC__icontains=params['search']), IS_ACTIVE=self.ACTIVE_DEFAULT_VALUE)
            else:
                queryset = UsageType.objects.filter(
                    IS_ACTIVE=self.ACTIVE_DEFAULT_VALUE)
            read_serializer = UsageTypeSerializer(queryset, many=True)
        return Response(read_serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        request.data["REC_ADD_BY"] = request.user.id
        request.data["REC_MOD_BY"] = request.user.id

        create_serializer = UsageTypeSerializer(data=request.data)
        if create_serializer.is_valid():
            new_product = create_serializer.save()
            # read_serializer = UsageTypeSerializer(new_product)
            # return Response(read_serializer.data, status=status.HTTP_201_CREATED)
            return Response({'success' : "Data is saved successfully" ,  'success_ur' : "ڈیٹا کامیابی سے محفوظ ہو گیا ہے۔" } , status=status.HTTP_201_CREATED)
        return Response(create_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id=None):
        try:
            product_to_update = UsageType.objects.get(USAGE_ID=id)
        except UsageType.DoesNotExist:
           return Response({'error': 'The Product Usage Type does not exist.' , "error_ur" : "پروڈکٹ کے استعمال کی قسم موجود نہیں ہے۔" }, status=status.HTTP_400_BAD_REQUEST)

        request.data["REC_ADD_BY"] = product_to_update.REC_ADD_BY
        request.data["REC_MOD_BY"] = request.user.id

        update_serializer = UsageTypeSerializer(
            product_to_update, data=request.data)
        if update_serializer.is_valid():
            updated_earning = update_serializer.save()
            # read_serializer = UsageTypeSerializer(updated_earning)
            # return Response(read_serializer.data, status=status.HTTP_200_OK)
            return Response({'success' : "Data is saved successfully" ,  'success_ur' : "ڈیٹا کامیابی سے محفوظ ہو گیا ہے۔" } , status=status.HTTP_200_OK)
        return Response(update_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):
        try:
            prod_to_delete = UsageType.objects.get(USAGE_ID=id)
        except UsageType.DoesNotExist:
            return Response({'error': 'The Product Usage Type does not exist.' , "error_ur" : "پروڈکٹ کے استعمال کی قسم موجود نہیں ہے۔" }, status=status.HTTP_400_BAD_REQUEST)

        prod_to_delete.REC_MOD_BY = request.user.id
        prod_to_delete.IS_ACTIVE = 0
        prod_to_delete.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
