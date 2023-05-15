from django.db.models import Q
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action, permission_classes
from accounts.CustomPermission import IsUserAllowed
from accounts.renderers import UserRenderer
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import Group
# models imports
from accounts.model.Account import Accounts
# serializers imports
from accounts.serializer.UsersSerializer import AccountsSerializer


class UserAccountsListView(
    APIView,  # Basic View class provided by the Django Rest Framework
    UpdateModelMixin,  # Mixin that allows the basic APIView to handle PUT HTTP requests
    # Mixin that allows the basic APIView to handle DELETE HTTP request):
    DestroyModelMixin,
):
    permission_classes = [IsUserAllowed({'POST': 'accounts.add_user', 'PUT': 'accounts.change_user',
                                        'DELETE': 'accounts.delete_user', 'GET': 'accounts.view_user'})]
    renderer_classes = [UserRenderer]
    rec_is_active = 1

    def get(self, request, id=None):
        if id:
            try:
                queryset = Accounts.objects.get(ACCT_ID=id)
            except Accounts.DoesNotExist:
                return Response({'error': 'The Account does not exist.'  , "error_ur" : "اکاؤنٹ موجود نہیں ہے۔" }, status=status.HTTP_400_BAD_REQUEST)
            read_serializer = AccountsSerializer(queryset)
        else:
            if request.query_params:
                params = request.query_params
                queryset = Accounts.objects.filter(Q(ACCT_TITLE__icontains=params['search']) | Q(ACCT_REF__icontains=params['search']) | Q(
                    ACCT_TYP__icontains=params['search']) | Q(ACCT_DESC__icontains=params['search']) | Q(ACCT_STS__icontains=params['search']))
            else:
                queryset = Accounts.objects.all()
            read_serializer = AccountsSerializer(queryset, many=True)
        return Response(read_serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        request.data["REC_ADD_BY"] = request.user.id
        request.data["REC_MOD_BY"] = request.user.id

        create_serializer = AccountsSerializer(data=request.data)
        if create_serializer.is_valid():
            new_account = create_serializer.save()
            # read_serializer = AccountsSerializer(new_account)
            # return Response(read_serializer.data, status=status.HTTP_201_CREATED)
            return Response({'success' : "Data is saved successfully" ,  'success_ur' : "ڈیٹا کامیابی سے محفوظ ہو گیا ہے۔" } , status=status.HTTP_201_CREATED)
        return Response(create_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id=None):
        try:
            acc_to_update = Accounts.objects.get(ACCT_ID=id)
        except Accounts.DoesNotExist:
            return Response({'error': 'The Account does not exist.'  , "error_ur" : "اکاؤنٹ موجود نہیں ہے۔" }, status=status.HTTP_400_BAD_REQUEST)

        request.data["REC_ADD_BY"] = acc_to_update.REC_ADD_BY
        request.data["REC_MOD_BY"] = request.user.id

        update_serializer = AccountsSerializer(
            acc_to_update, data=request.data)
        if update_serializer.is_valid():
            updated_account = update_serializer.save()
            # read_serializer = AccountsSerializer(updated_account)
            # return Response(read_serializer.data, status=status.HTTP_201_CREATED)
            return Response({'success' : "Data is saved successfully" ,  'success_ur' : "ڈیٹا کامیابی سے محفوظ ہو گیا ہے۔" } , status=status.HTTP_201_CREATED)
        return Response(update_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):
        try:
            acc_to_delete = Accounts.objects.get(ACCT_ID=id)
        except Accounts.DoesNotExist:
            return Response({'error': 'This Department item does not exist.'   , "error_ur" : "یہ محکمہ آئٹم موجود نہیں ہے۔" }, status=status.HTTP_400_BAD_REQUEST)
        if acc_to_delete.CLOSNG_BLNCE != 0:
            return Response( {'error': 'Cannot delete account due to non zero balance' , "error_ur" : "صفر بیلنس نہ ہونے کی وجہ سے اکاؤنٹ ڈیلیٹ نہیں کیا جا سکتا"  } , status=status.HTTP_400_BAD_REQUEST)

        acc_to_delete.REC_MOD_BY = request.user.id
        acc_to_delete.ACCT_STS = 0
        acc_to_delete.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


class AdvanceSearchAccount(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [AllowAny]

    def post(self, request, format=None, group_name=None):
        try:
            query_set = Accounts.objects.get(Q(ACCT_TITLE__iexact=request.data["ACCT_TITLE"]) | Q(
                ACCT_REF__iexact=request.data["ACCT_REF"]) | Q(CLOSNG_BLNCE__iexact=request.data["CLOSNG_BLNCE"]), USER_ID__isnull=False)
        except Accounts.DoesNotExist:
            return Response({"error" : "The Account does not exist" , "error_ur" : "اکاؤنٹ موجود نہیں ہے۔"}  , status=status.HTTP_404_NOT_FOUND)

        # user_serialzier = AccountsSerializer(query_set)
        # return Response(user_serialzier.data, status=status.HTTP_200_OK)
        return Response({'success' : "Data is saved successfully" ,  'success_ur' : "ڈیٹا کامیابی سے محفوظ ہو گیا ہے۔" } , status=status.HTTP_201_CREATED)


class AccountsByAcctType(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [AllowAny]

    def post(self, request, format=None, group_name=None):
        if group_name:
            try:
                grp_queryset = Group.objects.get(name=group_name)
            except Group.DoesNotExist:
                return Response({"error" : "The Account does not exist" , "error_ur" : "اکاؤنٹ موجود نہیں ہے۔"}  , status=status.HTTP_404_NOT_FOUND)
            query_set = Accounts.objects.filter(
                Q(ACCT_TYP__icontains=grp_queryset.id) | Q(USER_ID__isnull=True), ACCT_STS=1)
        else:
            query_set = Accounts.objects.filter(ACCT_STS=1)

        # user_serialzier = AccountsSerializer(query_set, many=True)
        # return Response(user_serialzier.data, status=status.HTTP_200_OK)
        return Response({'success' : "Data is saved successfully" ,  'success_ur' : "ڈیٹا کامیابی سے محفوظ ہو گیا ہے۔" } , status=status.HTTP_201_CREATED)
