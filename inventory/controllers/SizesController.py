from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from accounts.CustomPermission import IsUserAllowed
from accounts.renderers import UserRenderer
# models imports
from inventory.model.ProductSizes import ProductSizes
# serializers imports
from inventory.serializers.ProductSizesSerializer import ProductSizesSerializer
from inventory.serializers.UsageSizesSerializer import UsageSizesSerializer


class SizesListView(
    APIView,  # Basic View class provided by the Django Rest Framework
    UpdateModelMixin,  # Mixin that allows the basic APIView to handle PUT HTTP requests
    # Mixin that allows the basic APIView to handle DELETE HTTP request):
    DestroyModelMixin,
):
    permission_classes = [IsUserAllowed({'POST': 'productusagetype.add_productusagetype', 'PUT': 'productusagetype.change_productusagetype',
                                        'DELETE': 'productusagetype.delete_productusagetype', 'GET': 'productusagetype.view_productusagetype'})]
    renderer_classes = [UserRenderer]

    def get(self, request, id=None):
        if id:
            try:
                queryset = ProductSizes.objects.get(SIZE_ID=id)
            except ProductSizes.DoesNotExist:
                return Response({'error': 'The Usage Size does not exist.'  , "error_ur" : "استعمال کا سائز موجود نہیں ہے۔"}, status=status.HTTP_400_BAD_REQUEST)
            read_serializer = ProductSizesSerializer(queryset)
        else:
            if request.query_params:
                params = request.query_params
                queryset = ProductSizes.objects.filter(Q(WIDTH__icontains=params['search']) | Q(
                    LENGHT__icontains=params['search']) | Q(THICKNESS__icontains=params['search']))
            else:
                queryset = ProductSizes.objects.all()
            read_serializer = ProductSizesSerializer(queryset, many=True)
        return Response(read_serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        request.data["REC_ADD_BY"] = request.user.id
        request.data["REC_MOD_BY"] = request.user.id

        create_serializer = ProductSizesSerializer(data=request.data)
        if create_serializer.is_valid():
            new_product = create_serializer.save()
            # read_serializer = ProductSizesSerializer(new_product)
            # return Response(read_serializer.data, status=status.HTTP_201_CREATED)
            return Response({'success' : "Data is saved successfully" ,  'success_ur' : "ڈیٹا کامیابی سے محفوظ ہو گیا ہے۔" } , status=status.HTTP_201_CREATED)
        return Response(create_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id=None):
        try:
            product_to_update = ProductSizes.objects.get(SIZE_ID=id)
        except ProductSizes.DoesNotExist:
            return Response({'error': 'The Usage Size does not exist.'  , "error_ur" : "استعمال کا سائز موجود نہیں ہے۔"}, status=status.HTTP_400_BAD_REQUEST)

        request.data["REC_ADD_BY"] = product_to_update.REC_ADD_BY
        request.data["REC_MOD_BY"] = request.user.id

        update_serializer = ProductSizesSerializer(
            product_to_update, data=request.data)
        if update_serializer.is_valid():
            updated_earning = update_serializer.save()
            # read_serializer = ProductSizesSerializer(updated_earning)
            # return Response(read_serializer.data, status=status.HTTP_200_OK)
            return Response({'success' : "Data is saved successfully" ,  'success_ur' : "ڈیٹا کامیابی سے محفوظ ہو گیا ہے۔" } , status=status.HTTP_200_OK)
        return Response(update_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):
        try:
            prod_to_delete = ProductSizes.objects.get(SIZE_ID=id)
        except ProductSizes.DoesNotExist:
            return Response({'error': 'The Usage Size does not exist.'  , "error_ur" : "استعمال کا سائز موجود نہیں ہے۔" }, status=status.HTTP_400_BAD_REQUEST)

        prod_to_delete.REC_MOD_BY = request.user.id
        prod_to_delete.IS_ACTIVE = 0
        prod_to_delete.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
