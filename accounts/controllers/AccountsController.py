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
import math
from datetime import datetime
import pandas as pd
from django.db import connection
import json
# models imports
from accounts.model.Account import Accounts, User, Phone_Numbers  , Address , account_type
# util
from inventory.utility.DataConversion import dateConversion , acctTypeParams
from inventory.utility.Translation import func_en_to_ur , func_ur_to_en
# serializers imports
from accounts.serializer.UsersSerializer import AddAccountsSerializer, AccountsDetailExtraSerializer, AccountsDetailSerializer,UserDetailSerializer,AccountsSerializer ,UserRegistrationSerializer 
from accounts.serializer.PhNumberSerializer import PhNumberSerializer
from accounts.serializer.AddressSerializer import AddressSerializer

class AccountsListView(
    APIView,  # Basic View class provided by the Django Rest Framework
    UpdateModelMixin,  # Mixin that allows the basic APIView to handle PUT HTTP requests
    # Mixin that allows the basic APIView to handle DELETE HTTP request):
    DestroyModelMixin,
):
    permission_classes = [IsUserAllowed({'POST': 'accounts.add_user', 'PUT': 'accounts.change_user',
                                        'DELETE': 'accounts.delete_user', 'GET': 'accounts.view_user'})]
    rec_is_active = 1
    renderer_classes = [UserRenderer]

    def getOne(self, request, id):
        if id:
            try:
                query = """CALL `datafunc_Mabrle_ERP_wUrdu`.`ACCT_Detail`( 1 , """+str(id)+""");  """    
                acct = pd.read_sql(query, connection)
                if not acct.empty:
                    query = """CALL `datafunc_Mabrle_ERP_wUrdu`.`ACCT_Detail`( 2 , """+str(acct["USER_ID"][0])+""");  """    
                    address = pd.read_sql(query, connection)
                    query = """CALL `datafunc_Mabrle_ERP_wUrdu`.`ACCT_Detail`( 3 , """+str(acct["USER_ID"][0])+""");  """    
                    contact_info = pd.read_sql(query, connection)
                    query = """CALL `datafunc_Mabrle_ERP_wUrdu`.`ACCT_Detail`( 4 , """+str(acct["ACCT_ID"][0])+""");  """    
                    acc_type = pd.read_sql(query, connection)
                    query = """CALL `datafunc_Mabrle_ERP_wUrdu`.`ACCT_Detail`( 5 , """+str(acct["USER_ID"][0])+""");  """    
                    roles = pd.read_sql(query, connection)

            except ConnectionError:
                return Response( {"error" : "Database Connection Error" , "error_ur" :  "ڈیٹا بیس کنکشن کی خرابی " }  , status=status.HTTP_400_BAD_REQUEST)


        if acct.empty:
            return Response( {"error" : "No record found" , "error_ur" : "کوئی ریکارڈ نہیں ملا" }  , status=status.HTTP_400_BAD_REQUEST)
        else:
            acct_data=acct.to_dict(orient='records')[0]
            acct_data['addresses'] = address.to_dict(orient='records')
            acct_data['contact_info'] = contact_info.to_dict(orient='records')
            acct_data['acct_type'] = acc_type.to_dict(orient='records')
            acct_data['roles'] = roles.to_dict(orient='records')
            return Response(acct_data, status=status.HTTP_200_OK)


    def getAll(self):
        return Accounts.objects.all()

    def searchActive(self, params):
        page = int(params.get('page' , 1) ) 
        parPage = params.get('perPage')
        start = (page - 1) * int(parPage)
        end = page * int(parPage)
        q = params.get('q') 
        q = dateConversion(q)
        if 'ACCT_TYP' in params:
            queryset = Accounts.objects.filter(Q(ACCT_TITLE__icontains=q) | Q(ACCT_TITLE_UR__icontains=q) | Q(ACCT_REF__icontains=q) |
                   Q(ACCT_REF_UR__icontains=q)  | Q(ACCT_DESC__icontains=q)  | Q(ACCT_DESC_UR__icontains=q) | Q(ACCT_CREATE_DT__icontains = q ) | Q(OPNG_BLNCE__icontains=q) | Q(CLOSNG_BLNCE__icontains=q) ,   Q(acct_type__ACCT_TYPE_NM__icontains = params["ACCT_TYP"])  )        
        else:
            queryset = Accounts.objects.filter(Q(ACCT_TITLE__icontains=q) | Q(ACCT_TITLE_UR__icontains=q) | Q(ACCT_REF__icontains=q) |
                   Q(ACCT_REF_UR__icontains=q)  | Q(ACCT_DESC__icontains=q)  | Q(ACCT_DESC_UR__icontains=q) | Q(ACCT_CREATE_DT__icontains= q  ) | Q(OPNG_BLNCE__icontains=q) | Q(CLOSNG_BLNCE__icontains=q)   )
        total = queryset.count()
        read_serializer = AccountsDetailExtraSerializer( queryset[start:end] , many=True )
        return Response({'data' :read_serializer.data , 'total' : total , 'Page' : page , 'last_Page' : math.ceil( total / int(parPage) )  }, status=status.HTTP_200_OK , )
        


        

        
    def get(self, request, id=None):
        if id:
            return self.getOne(request, id)
        elif request.query_params:
            return self.searchActive(params=request.query_params)
        else:
            queryset = self.getAll()
        read_serializer = AccountsDetailExtraSerializer(queryset, many=True)
        return Response(read_serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if request.data:
            request.data["REC_ADD_BY"] = request.user.id
            request.data["REC_MOD_BY"] = request.user.id
            if "Non_User" in request.data:
                request.data["account"]["REC_ADD_BY"] = request.user.id
                request.data["account"]["REC_MOD_BY"] = request.user.id
                create_serializer =  AddAccountsSerializer(data= request.data["account"])
                if create_serializer.is_valid():
                    new_user = create_serializer.save()
                    # user_serializer = AccountsDetailSerializer(new_user)
                    # return Response(user_serializer.data, status=status.HTTP_201_CREATED)
                    return Response({'success' : "Account is created successfully" ,  'success_ur' : "اکاؤنٹ کامیابی سے بن گیا ہے۔" } , status=status.HTTP_201_CREATED)
                return Response(create_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            name = request.data["account"]["ACCT_TITLE"]
            request.data["FIRST_NAME"] = " ".join(name.split(" ")[:-1]) 
            request.data["LAST_NAME"]  = name.split(" ")[-1]
        create_serializer = UserRegistrationSerializer(data=request.data)
        if create_serializer.is_valid():
            new_user = create_serializer.save()
            # user_serializer = UserDetailSerializer(new_user)
            # return Response(user_serializer.data, status=status.HTTP_201_CREATED)
            return Response({'success' : "Account is created successfully" ,  'success_ur' : "اکاؤنٹ کامیابی سے بن گیا ہے۔" } , status=status.HTTP_201_CREATED)
        return Response(create_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id=None):
        ph_check = True 
        addrs_check = True  
        # For bypassing the email already exist validation
        unique_words = "11b1b1b1b1b"
        try:
            acct = Accounts.objects.get(ACCT_ID=id)
            acc_to_update = User.objects.get(email=acct.USER_ID)   
        except User.DoesNotExist:
            return Response({ 'error': 'The User does not exist.' , 'error_ur': 'صارف موجود نہیں ہے۔' }, status=status.HTTP_400_BAD_REQUEST)
        request.data["REC_ADD_BY"] = acc_to_update.REC_ADD_BY
        request.data["REC_MOD_BY"] = request.user.id
        # updating the Non-User Account
        if "Non_User" in request.data:
            try:
                acc_to_update = Accounts.objects.get(ACCT_ID=id)
            except User.DoesNotExist:
                return Response({ 'error': 'The User does not exist.' , 'error_ur': 'صارف موجود نہیں ہے۔' }, status=status.HTTP_400_BAD_REQUEST) 
            create_serializer =  AddAccountsSerializer(acc_to_update ,data= request.data["account"])
            if create_serializer.is_valid():
                new_user = create_serializer.save()
                return Response({'success' : "Account is updated successfully" ,  'success_ur' : "اکاؤنٹ کامیابی کے ساتھ اپ ڈیٹ ہو گیا ہے۔" } , status=status.HTTP_200_OK)
            return Response(create_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        name = request.data["account"]["ACCT_TITLE"]
        request.data["FIRST_NAME"] = " ".join(name.split(" ")[:-1]) 
        request.data["LAST_NAME"]  = name.split(" ")[-1]
        email = request.data["email"]
        request.data["email"] = unique_words + email
        try:
            user_addresses = request.data["addresses"]
            user_contact_info = request.data["contact_info"]
        except:
            pass            
        update_serializer = UserRegistrationSerializer(acc_to_update, data=request.data)
        if update_serializer.is_valid():
            updated_account = update_serializer.save()
            # Update address
            # Delete Address that are not present in the address data 
            try:
                existing_addrs = Address.objects.filter(USER=updated_account.id)
                existing_ids = set(item.ADDR_ID for item in existing_addrs)
                request_ids = set(item.get('ADDR_ID') for item in user_addresses)
                ids_to_delete = existing_ids - request_ids
                if ids_to_delete:
                    addresses_to_del =  Address.objects.filter(ADDR_ID__in=ids_to_delete).delete() 
            except Address.DoesNotExist:
                pass 
            for addr in user_addresses:             
                addr["USER"] = updated_account.id
                if addrs_check is True :
                    addr["IS_PRIMARY"] = 1
                    addrs_check = False
                else:
                    addr["IS_PRIMARY"] = 0
                # Updating the existing one address
                if "ADDR_ID" in addr:
                    address_to_update =  Address.objects.get(ADDR_ID=addr["ADDR_ID"])
                    create_addr_serializer = AddressSerializer(address_to_update, data=addr)
                    if create_addr_serializer.is_valid():
                        create_addr_serializer.save()
                    else:
                        return Response(create_addr_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    # add new address
                    create_addr_serializer = AddressSerializer(data=addr)
                    if create_addr_serializer.is_valid():
                        create_addr_serializer.save()
                    else:
                        return Response(create_addr_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Update Phone_Numbers
            # Delete Phone_Numbers that are not present in the Phone_Numbers data 
            try:
                existing_nmbrs = Phone_Numbers.objects.filter(USER=updated_account.id)
                existing_ids = set(item.PH_ID for item in existing_nmbrs)
                request_ids = set(item.get('PH_ID') for item in user_contact_info)
                ids_to_delete = existing_ids - request_ids
                if ids_to_delete:
                   Phone_Numbers.objects.filter(PH_ID__in=ids_to_delete).delete() 
            except Phone_Numbers.DoesNotExist:
                pass 
            for nmbrr in user_contact_info:             
                nmbrr["USER"] = updated_account.id
                if ph_check is True :
                    nmbrr["IS_PRIMARY"] = 1
                    ph_check = False
                else:
                    nmbrr["IS_PRIMARY"] = 0
                # Updating the existing one address
                if "PH_ID" in nmbrr:
                    nmbrr_to_update =  Phone_Numbers.objects.get(PH_ID=nmbrr["PH_ID"])
                    create_nmbrr_serializer = PhNumberSerializer(nmbrr_to_update, data=nmbrr)
                    if create_nmbrr_serializer.is_valid():
                        create_nmbrr_serializer.save()
                    else:
                        return Response(create_nmbrr_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    # add new address
                    create_nmbrr_serializer = PhNumberSerializer(data=nmbrr)
                    if create_nmbrr_serializer.is_valid():
                        create_nmbrr_serializer.save()
                    else:
                        return Response(create_nmbrr_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            # read_serializer = UserDetailSerializer(updated_account)
            # return Response(read_serializer.data, status=status.HTTP_201_CREATED)
            return Response({'success' : "Account is updated successfully" ,  'success_ur' : "اکاؤنٹ کامیابی کے ساتھ اپ ڈیٹ ہو گیا ہے۔" } , status=status.HTTP_200_OK)
        return Response(update_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):
        try:
            acc_to_delete = Accounts.objects.get(ACCT_ID=id)
        except Accounts.DoesNotExist:
            return Response({ 'error': 'The User does not exist.' , 'error_ur': 'صارف موجود نہیں ہے۔' }, status=status.HTTP_400_BAD_REQUEST)

        if acc_to_delete.CLOSNG_BLNCE != 0:
            return Response({'error': 'Cannot delete account due to non zero balance' , 'error_ur': 'صفر بیلنس نہ ہونے کی وجہ سے اکاؤنٹ ڈیلیٹ نہیں کیا جا سکتا'}, 
            status=status.HTTP_400_BAD_REQUEST)

        acc_to_delete.REC_MOD_BY = request.user.id
        acc_to_delete.IS_ACTIVE = 0
        acc_to_delete.save()

        return Response({'success' : "Account is deleted successfully" ,  'success_ur' : "اکاؤنٹ کامیابی کے ساتھ حذف ہو گیا ہے۔" } , status=status.HTTP_200_OK)


class AdvanceSearchAccount(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [AllowAny]

    def post(self, request, format=None, group_name=None):
        try:
            query_set = Accounts.objects.get(Q(ACCT_TITLE__iexact=request.data["ACCT_TITLE"]) | Q(
                ACCT_REF__iexact=request.data["ACCT_REF"]) | Q(CLOSNG_BLNCE__iexact=request.data["CLOSNG_BLNCE"]), USER_ID__isnull=False)
        except Accounts.DoesNotExist:
            return Response({ 'error': 'The Account does not exist.' , 'error_ur': 'صارف موجود نہیں ہے۔' } , status=status.HTTP_404_NOT_FOUND)

        user_serialzier = AccountsSerializer(query_set)
        return Response(user_serialzier.data, status=status.HTTP_200_OK)


class AccountsByAcctType(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [AllowAny]

    def post(self, request, format=None, group_name=None):
        if group_name:
            try:
                grp_queryset = Group.objects.get(name=group_name)
            except Group.DoesNotExist:
                return Response({ 'error': 'The Account does not exist.' , 'error_ur': 'صارف موجود نہیں ہے۔' }, status=status.HTTP_404_NOT_FOUND)
            query_set = Accounts.objects.filter(
                Q(ACCT_TYP__icontains=grp_queryset.id) | Q(USER_ID__isnull=True), ACCT_STS=1)
        else:
            query_set = Accounts.objects.filter(ACCT_STS=1)
            # return Response({'success' : "Data is saved successfully" ,  'success_ur' : "ڈیٹا کامیابی سے محفوظ ہو گیا ہے۔" } , status=status.HTTP_200_OK)
        user_serialzier = AccountsSerializer(query_set, many=True)
        return Response(user_serialzier.data, status=status.HTTP_200_OK)
