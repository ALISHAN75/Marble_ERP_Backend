from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import AllowAny
from accounts.renderers import UserRenderer
# models imports
from finance.model.Currency import Currency
# serializers imports
from finance.serializer.CurrencySerializer import CurrencySerializer


class CurrencyItemListView(
    APIView,  # Basic View class provided by the Django Rest Framework
    UpdateModelMixin,  # Mixin that allows the basic APIView to handle PUT HTTP requests
    # Mixin that allows the basic APIView to handle DELETE HTTP request):
    DestroyModelMixin,
):
    permission_classes = [AllowAny]
    renderer_classes = [UserRenderer]
    rec_is_active = 1

    def get(self, request, id=None):
        if id:
            try:
                queryset = Currency.objects.get(CURNCY_ID=id)
            except Currency.DoesNotExist:
                return Response({'error': 'The currency does not exist.' , "error_ur" :"کرنسی موجود نہیں ہے۔"  }, status=status.HTTP_400_BAD_REQUEST)
            read_serializer = CurrencySerializer(queryset)
        else:
            queryset = Currency.objects.all()
            read_serializer = CurrencySerializer(queryset, many=True)
        return Response(read_serializer.data, status=status.HTTP_200_OK)
        

    # def post(self, request):
    #     request.data["REC_ADD_BY"] = request.user.id

    #     create_serializer = CurrencySerializer(data=request.data)
    #     if create_serializer.is_valid():
    #         new_expense_transc = create_serializer.save()
    #         # read_serializer = CurrencySerializer(new_expense_transc)
    #         # return Response(read_serializer.data, status=status.HTTP_201_CREATED)
    #         return Response({'success' : "Data is saved successfully" ,  'success_ur' : "ڈیٹا کامیابی سے محفوظ ہو گیا ہے۔" } , status=status.HTTP_201_CREATED)
    #     return Response(create_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def put(self, request, id=None):
    #     try:
    #         earning_to_update = Currency.objects.get(CURNCY_ID=id)
    #     except Currency.DoesNotExist:
    #         return Response({'error': 'The Expense Transaction does not exist.'  , "error_ur" :"اخراجات کا لین دین موجود نہیں ہے۔" }, status=status.HTTP_400_BAD_REQUEST)
    #     request.data["REC_ADD_BY"] = earning_to_update.REC_ADD_BY

    #     update_serializer = CurrencySerializer(
    #         earning_to_update, data=request.data)
    #     if update_serializer.is_valid():
    #         updated_earning = update_serializer.save()
    #         return Response({'success' : "Data is saved successfully" ,  'success_ur' : "ڈیٹا کامیابی سے محفوظ ہو گیا ہے۔" } , status=status.HTTP_201_CREATED)
    #         # read_serializer = CurrencySerializer(updated_earning)
    #         # return Response(read_serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(update_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, id=None):
    #     try:
    #         earning_to_delete = Currency.objects.get(CURNCY_ID=id)
    #     except Currency.DoesNotExist:
    #         return Response({'error': 'This Earning item does not exist.' , "error_ur" :"یہ کمائی والی چیز موجود نہیں ہے۔" }, status=status.HTTP_400_BAD_REQUEST)
    #     earning_to_delete.IS_ACTIVE = 0
    #     earning_to_delete.save()

    #     return Response(None, status=status.HTTP_204_NO_CONTENT)
