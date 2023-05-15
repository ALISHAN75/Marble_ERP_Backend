from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from accounts.renderers import UserRenderer
# models imports
from finance.model.Expense_Transactions import Expense_Transaction_Items
# serializers imports
from finance.serializer.ExpenseTransItemsSerializer import ExpenseTransItemsSerializer


class ExpenseTransItemListView(
    APIView,  # Basic View class provided by the Django Rest Framework
    UpdateModelMixin,  # Mixin that allows the basic APIView to handle PUT HTTP requests
    # Mixin that allows the basic APIView to handle DELETE HTTP request):
    DestroyModelMixin,
):
    rec_is_active = 1
    renderer_classes = [UserRenderer]

    def get(self, request, id=None):
        if id:
            try:
                queryset = Expense_Transaction_Items.objects.get(
                    EXPNS_TRANS_ITEM_ID=id)
            except Expense_Transaction_Items.DoesNotExist:
                return Response({'error': 'The Expense Transaction does not exist.'  , "error_ur" : "اخراجات کا لین دین موجود نہیں ہے۔"}, status=status.HTTP_400_BAD_REQUEST)
            read_serializer = ExpenseTransItemsSerializer(queryset)
        else:
            if request.query_params:
                params = request.query_params
                queryset = Expense_Transaction_Items.objects.filter(
                    Q(PYMNT_AMNT__icontains=params['search']) | Q(PYMNT_DT__icontains=params['search']))
            else:
                queryset = Expense_Transaction_Items.objects.all()
            read_serializer = ExpenseTransItemsSerializer(queryset, many=True)
        return Response(read_serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        request.data["REC_ADD_BY"] = request.user.id

        create_serializer = ExpenseTransItemsSerializer(data=request.data)
        if create_serializer.is_valid():
            new_expense_transc = create_serializer.save()
            read_serializer = ExpenseTransItemsSerializer(new_expense_transc)
            return Response(read_serializer.data, status=status.HTTP_201_CREATED)
        return Response(create_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id=None):
        try:
            earning_to_update = Expense_Transaction_Items.objects.get(
                EARN_TRANS_ID=id)
        except Expense_Transaction_Items.DoesNotExist:
            return Response({'error': 'The Expense Transaction does not exist.'  , "error_ur" : "اخراجات کا لین دین موجود نہیں ہے۔"}, status=status.HTTP_400_BAD_REQUEST)
        request.data["REC_ADD_BY"] = earning_to_update.REC_ADD_BY

        update_serializer = ExpenseTransItemsSerializer(
            earning_to_update, data=request.data)
        if update_serializer.is_valid():
            updated_earning = update_serializer.save()
            read_serializer = ExpenseTransItemsSerializer(updated_earning)
            return Response(read_serializer.data, status=200)
        return Response(update_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):
        try:
            earning_to_delete = Expense_Transaction_Items.objects.get(
                EMP_DEPT_ID=id)
        except Expense_Transaction_Items.DoesNotExist:
            return Response({'error': 'The Expense Transaction does not exist.'  , "error_ur" : "اخراجات کا لین دین موجود نہیں ہے۔"}, status=status.HTTP_400_BAD_REQUEST)
        earning_to_delete.IS_ACTIVE = 0
        earning_to_delete.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
