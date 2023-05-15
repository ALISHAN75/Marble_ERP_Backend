from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from accounts.CustomPermission import IsUserAllowed
from accounts.renderers import UserRenderer
# models imports
from inventory.model.ProductCategory import ProductCategory
# serializers imports
from inventory.serializers.ProductCategorySerializer import ProductCategorySerializer


class ProductCategoryListView(
    APIView,  # Basic View class provided by the Django Rest Framework
    UpdateModelMixin,  # Mixin that allows the basic APIView to handle PUT HTTP requests
    # Mixin that allows the basic APIView to handle DELETE HTTP request):
    DestroyModelMixin,
):
    permission_classes = [IsUserAllowed({'POST': 'productcategory.add_productcategory', 'PUT': 'productcategory.change_productcategory',
                                        'DELETE': 'productcategory.delete_productcategory', 'GET': 'productcategory.view_productcategory'})]
    renderer_classes = [UserRenderer]
    ACTIVE_DEFAULT_VALUE = 1

    def get(self, request, id=None):
        if id:
            try:
                queryset = ProductCategory.objects.get(CAT_ID=id)
            except ProductCategory.DoesNotExist:
                return Response({'error': 'The Product Category does not exist.'  , "error_ur" : "پروڈکٹ کا زمرہ موجود نہیں ہے۔" }, status=status.HTTP_400_BAD_REQUEST)
            read_serializer = ProductCategorySerializer(queryset)

        else:
            if request.query_params:
                params = request.query_params
                queryset = ProductCategory.objects.filter(Q(CAT_NM__icontains=params['search']) | Q(
                    CAT_DESC__icontains=params['search']), IS_ACTIVE=self.ACTIVE_DEFAULT_VALUE)
            else:
                queryset = ProductCategory.objects.filter(
                    IS_ACTIVE=self.ACTIVE_DEFAULT_VALUE)
            read_serializer = ProductCategorySerializer(queryset, many=True)
        return Response(read_serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        request.data["REC_ADD_BY"] = request.user.id
        request.data["REC_MOD_BY"] = request.user.id

        create_serializer = ProductCategorySerializer(data=request.data)

        if create_serializer.is_valid():
            new_product = create_serializer.save()
            # read_serializer = ProductCategorySerializer(new_product)
            # return Response(read_serializer.data, status=status.HTTP_201_CREATED)
            return Response({'success' : "Data is saved successfully" ,  'success_ur' : "ڈیٹا کامیابی سے محفوظ ہو گیا ہے۔" } , status=status.HTTP_201_CREATED)
        return Response(create_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id=None):
        try:
            product_to_update = ProductCategory.objects.get(CAT_ID=id)
        except ProductCategory.DoesNotExist:
            return Response({'error': 'The Product Category does not exist.'  , "error_ur" : "پروڈکٹ کا زمرہ موجود نہیں ہے۔" }, status=status.HTTP_400_BAD_REQUEST)

        request.data["REC_ADD_BY"] = product_to_update.REC_ADD_BY
        request.data["REC_MOD_BY"] = request.user.id

        update_serializer = ProductCategorySerializer(
            product_to_update, data=request.data)
        if update_serializer.is_valid():
            updated_earning = update_serializer.save()
            # read_serializer = ProductCategorySerializer(updated_earning)
            # return Response(read_serializer.data, status=status.HTTP_200_OK)
            return Response({'success' : "Data is saved successfully" ,  'success_ur' : "ڈیٹا کامیابی سے محفوظ ہو گیا ہے۔" } , status=status.HTTP_201_CREATED)
        return Response(update_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):
        try:
            prod_to_delete = ProductCategory.objects.get(CAT_ID=id)
        except ProductCategory.DoesNotExist:
           return Response({'error': 'The Product Category does not exist.'  , "error_ur" : "پروڈکٹ کا زمرہ موجود نہیں ہے۔" }, status=status.HTTP_400_BAD_REQUEST)

        prod_to_delete.REC_MOD_BY = request.user.id
        prod_to_delete.IS_ACTIVE = 0
        prod_to_delete.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
