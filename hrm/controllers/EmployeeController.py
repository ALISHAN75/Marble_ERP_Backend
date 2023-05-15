from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from accounts.CustomPermission import IsUserAllowed
from accounts.serializer.UsersSerializer import UserRegistrationSerializer
from accounts.renderers import UserRenderer
from rest_framework.permissions import AllowAny
# util
import math
import pandas as pd
from django.db import connection
from django.conf import settings
from inventory.utility.DataConversion import dateConversion
from accounts.renderers import UserRenderer
# models imports
from hrm.model.Employee import Employee, Employee_Compensation
from accounts.model.Account import Accounts, User
from accounts.model.Account import Phone_Numbers , Address
# serializers imports
from hrm.serializer.EmployeeSerializer import EmployeeSerializer
from hrm.serializer.EmployeeCompensationSerializer import EmployeeCompensationSerializer
from accounts.serializer.UsersSerializer import UserRegistrationSerializer 
from accounts.serializer.PhNumberSerializer import PhNumberSerializer
from accounts.serializer.AddressSerializer import AddressSerializer

class EmployeeListView(
    APIView,  # Basic View class provided by the Django Rest Framework
    UpdateModelMixin,  # Mixin that allows the basic APIView to handle PUT HTTP requests
    DestroyModelMixin,  # Mixin that allows the basic APIView to handle DELETE HTTP requests
):
    permission_classes = [IsUserAllowed({'POST': 'hrm.add_employees', 'PUT': 'hrm.change_employees',
                                        'DELETE': 'hrm.delete_employees', 'GET': 'hrm.view_employees'})]
    renderer_classes = [UserRenderer]
    rec_is_active = 1



    def getOne(self, request, id):
        if id:
            try:
                query = """ CALL `datafunc_Mabrle_ERP_wUrdu`.`HRM_Employee`(1 , """+str(id)+""", 0 , 0 ); """     
                employee = pd.read_sql(query, connection)
                if not employee.empty:
                    query = """ CALL `datafunc_Mabrle_ERP_wUrdu`.`HRM_Employee`(4 , """+str(id)+""", 0 , 0 ); """     
                    cmpnstion = pd.read_sql(query, connection)
                    query = """CALL `datafunc_Mabrle_ERP_wUrdu`.`ACCT_Detail`( 2 , """+str(employee["USER_ID"][0])+""");  """    
                    address = pd.read_sql(query, connection)
                    query = """CALL `datafunc_Mabrle_ERP_wUrdu`.`ACCT_Detail`( 3 , """+str(employee["USER_ID"][0])+""");  """    
                    contact_info = pd.read_sql(query, connection)
                    query = """CALL `datafunc_Mabrle_ERP_wUrdu`.`ACCT_Detail`( 4 , """+str(employee["ACCT_ID"][0])+""");  """    
                    acc_type = pd.read_sql(query, connection)
                    query = """CALL `datafunc_Mabrle_ERP_wUrdu`.`ACCT_Detail`( 5 , """+str(employee["USER_ID"][0])+""");  """    
                    roles = pd.read_sql(query, connection)
            except ConnectionError:
                return Response({"error" : "Database Connection Error" , "error_ur" :  "ڈیٹا بیس کنکشن کی خرابی " }, status=status.HTTP_400_BAD_REQUEST)

        if employee.empty:
            return Response({"error" : "No record found" , "error_ur" : "کوئی ریکارڈ نہیں ملا" }, status=status.HTTP_400_BAD_REQUEST)
        else:
            employee = employee.fillna('')
            employee_data=employee.to_dict(orient='records')[0]
            employee_data['EMP_COMPENSATION'] = cmpnstion.to_dict(orient='records')
            employee_data['addresses'] = address.to_dict(orient='records')
            employee_data['contact_info'] = contact_info.to_dict(orient='records')
            employee_data['acct_type'] = acc_type.to_dict(orient='records')
            employee_data['roles'] = roles.to_dict(orient='records')
            return Response(employee_data  , status=status.HTTP_200_OK)

             

    def getAll(self):
        try:
            query = """ CALL `datafunc_Mabrle_ERP_wUrdu`.`HRM_Employee`(2, 1, 1, 100000 ); """    
            my_data = pd.read_sql(query, connection)
        except ConnectionError:
            return Response({"error" : "Database Connection Error" , "error_ur" :  "ڈیٹا بیس کنکشن کی خرابی " }, status=status.HTTP_400_BAD_REQUEST)
        if my_data.empty:
            return Response({"error" : "No record found" , "error_ur" : "کوئی ریکارڈ نہیں ملا" }, status=status.HTTP_400_BAD_REQUEST)
        else:
            my_data = my_data.fillna('')
            return Response(my_data.to_dict(orient='records'), status=status.HTTP_200_OK)

    def searchActive(self, params):
        is_id_srch = 0
        page = int(params.get('page' , 1) ) 
        parPage = params.get('perPage' , 10)
        q = params.get('q' , '') 
        if len(q)>0:
            is_id_srch = 3
            q = dateConversion(q)
        else:
            is_id_srch = 2
        try:
            query = """ CALL `datafunc_Mabrle_ERP_wUrdu`.`HRM_Employee`("""+str(is_id_srch)+""", '"""+q+"""', """+str(page)+""", """+str(parPage)+""" ); """       
            my_data = pd.read_sql(query, connection)
            query = """ select FOUND_ROWS() """       
            total = pd.read_sql(query, connection)
        except ConnectionError:
                return Response({"error" : "Database Connection Error" , "error_ur" :  "ڈیٹا بیس کنکشن کی خرابی " }, status=status.HTTP_400_BAD_REQUEST)

        if my_data.empty:
            return Response([], status=status.HTTP_200_OK)
        else:      
            total = total.iloc[0,0]
            my_data = my_data.fillna('')
            return Response({'data' :my_data.to_dict(orient='records'), 'total' : total , 'Page' : page , 'last_Page' : math.ceil( total / int(parPage) )  }, status=status.HTTP_200_OK  )        
        
    def get(self, request, id=None):
        if id:
            return self.getOne(request, id)
        elif request.query_params:
            return self.searchActive(params=request.query_params)
        else:
            return self.getAll()



    def post(self, request):
        if request.data:
            try:
                emp_cmpnstion = request.data["EMP_COMPENSATION"] 
                request.data["REC_ADD_BY"] = request.user.id
                request.data["REC_MOD_BY"] = request.user.id
                name = request.data["USER"]["account"]["ACCT_TITLE"]
                request.data["EMP_FULL_NM"] = name
                request.data["USER"]["FIRST_NAME"]  = " ".join(name.split(" ")[:-1]) 
                request.data["USER"]["LAST_NAME"]  = name.split(" ")[-1]
                request.data["USER"]["REC_ADD_BY"] = request.user.id
                request.data["USER"]["REC_MOD_BY"] = request.user.id

            except:
                pass
        create_emp_serilaizer = EmployeeSerializer(data=request.data)
        if create_emp_serilaizer.is_valid():
            new_employee = create_emp_serilaizer.save()
            if len(emp_cmpnstion) > 0:
                for emp_cmp in emp_cmpnstion:
                    emp_cmp["EMP_ID"] = new_employee.EMP_ID
                    emp_cmp["REC_ADD_BY"] = request.user.id
                    emp_cmp["REC_MOD_BY"] = request.user.id
                    cmpstn_serilaizer = EmployeeCompensationSerializer(data=emp_cmp)
                    if cmpstn_serilaizer.is_valid():
                        cmpstn_serilaizer.save()
                    else:
                        return Response(cmpstn_serilaizer.errors, status=400)
            # read_emp_seriaizer = EmployeeSerializer(new_employee)
            # return Response(read_emp_seriaizer.data, status=201)
            return Response({'success' : "Data is saved successfully" ,  'success_ur' : "ڈیٹا کامیابی سے محفوظ ہو گیا ہے۔" } , status=status.HTTP_201_CREATED)
        return Response(create_emp_serilaizer.errors, status=400)


    def put(self, request, id=None):
        ph_check = True 
        addrs_check = True 
        unique_words = "11b1b1b1b1b"
        try:
            emp_to_update = Employee.objects.get(EMP_ID=id)          
        except Employee.DoesNotExist:
            return Response({'error': 'The Employee does not exist.' , "error_ur" : "ملازم موجود نہیں ہے۔"}, status=400)            
        request.data["REC_ADD_BY"] = emp_to_update.REC_ADD_BY
        request.data["REC_MOD_BY"] = request.user.id
        try:
            emp_cmpnstion = request.data["EMP_COMPENSATION"] 
            name = request.data["USER"]["account"]["ACCT_TITLE"]
            email = request.data["USER"]["email"]
            request.data["EMP_FULL_NM"] = name
            request.data["USER"]["email"] = unique_words + email
            request.data["USER"]["FIRST_NAME"]  = " ".join(name.split(" ")[:-1]) 
            request.data["USER"]["LAST_NAME"]  = name.split(" ")[-1]
            request.data["USER"]["REC_ADD_BY"] = emp_to_update.REC_ADD_BY
            request.data["USER"]["REC_MOD_BY"] = request.user.id            
            user_addresses = request.data["USER"]["addresses"]
            user_contact_info = request.data["USER"]["contact_info"]
        except:
            pass
        create_emp_serilaizer = EmployeeSerializer(emp_to_update, data=request.data)
        if create_emp_serilaizer.is_valid():
            new_employee = create_emp_serilaizer.save()
            if len(emp_cmpnstion) > 0:
                for emp_cmp in emp_cmpnstion:
                    if "EMP_CMPNSTN_ID" in emp_cmp:
                        emp_cmp["EMP_ID"] = emp_to_update.EMP_ID
                        emp_cmp["REC_MOD_BY"] = request.user.id
                        cmpnstn_to_update = Employee_Compensation.objects.get( EMP_CMPNSTN_ID = emp_cmp["EMP_CMPNSTN_ID"] , EMP_ID=id)
                        emp_cmp["REC_ADD_BY"] = cmpnstn_to_update.REC_ADD_BY
                        cmpstn_serilaizer = EmployeeCompensationSerializer(cmpnstn_to_update , data=emp_cmp)
                        if cmpstn_serilaizer.is_valid():
                            cmpstn_serilaizer.save()
                        else:
                            return Response(cmpstn_serilaizer.errors, status=400)
            # Add data in user accounts tables  
            try:
                acc_to_update = User.objects.get(email=emp_to_update.USER_ID)   
            except User.DoesNotExist:
                return Response({ 'error': 'The User does not exist.' , 'error_ur': 'صارف موجود نہیں ہے۔' }, status=status.HTTP_400_BAD_REQUEST)          
            update_serializer = UserRegistrationSerializer(acc_to_update, data=request.data["USER"])
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

            # read_emp_seriaizer = EmployeeSerializer(new_employee)
            # return Response(read_emp_seriaizer.data, status=201)
            return Response({'success' : "Employee is updated successfully" ,  'success_ur' : "ملازم کو کامیابی کے ساتھ اپ ڈیٹ کر دیا گیا ہے۔" } , status=status.HTTP_201_CREATED)
        return Response(create_emp_serilaizer.errors, status=400)
    


    def delete(self, request, id=None):
        try:
            emp_to_delete = Employee.objects.get(EMP_ID=id)
            user_acct_to_update = User.objects.get(email=emp_to_delete.USER_ID)
            acct_to_update = Accounts.objects.get(USER_ID=emp_to_delete.USER_ID)
        except:
           return Response({'error': 'The Employee does not exist.' , "error_ur" : "ملازم موجود نہیں ہے۔"}, status=400)              
        if acct_to_update.CLOSNG_BLNCE != 0:
            return Response({'error': 'Cannot delete account due to non zero balance' , 'error_ur': 'صفر بیلنس نہ ہونے کی وجہ سے اکاؤنٹ ڈیلیٹ نہیں کیا جا سکتا'}, 
            status=status.HTTP_400_BAD_REQUEST)

        emp_to_delete.REC_MOD_BY = request.user.id
        emp_to_delete.EMP_STS = 0
        emp_to_delete.IS_ACTIVE = 0
        emp_to_delete.save()

        

        user_acct_to_update.REC_MOD_BY = request.user.id
        user_acct_to_update.is_active = 0
        user_acct_to_update.save()
        
        acct_to_update.REC_MOD_BY = request.user.id
        acct_to_update.IS_ACTIVE = 0
        acct_to_update.save()


        return Response({'success' : "Employee is deleted successfully" ,  'success_ur' : "ملازم کامیابی کے ساتھ حذف ہو گیا ہے۔" } , status=status.HTTP_200_OK)


class AdvanceSearchEmployee(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [AllowAny]

    def post(self, request, format=None, group_name=None):
        try:
            query_set = Employee.objects.get(Q(USER_ID__FIRST_NAME__iexact=request.data["FIRST_NAME"]) | Q(USER_ID__LAST_NAME__iexact=request.data["LAST_NAME"]) | Q(
                EMP_DESIG_ID__DESIG_NM__iexact=request.data["DESIG_NM"]) | Q(EMP_TYP_ID__EMP_TYP_NM__iexact=request.data["EMP_TYP_NM"]) | Q(CNIC__iexact=request.data["CNIC"]))
        except Employee.DoesNotExist:
            return Response({'error': 'The Employee does not exist.' , "error_ur" : "ملازم موجود نہیں ہے۔"}  ,  status=status.HTTP_404_NOT_FOUND)

        # user_serialzier = EmployeeSerializer(query_set)
        # return Response(user_serialzier.data, status=status.HTTP_200_OK)
        return Response({'success' : "Data is saved successfully" ,  'success_ur' : "ڈیٹا کامیابی سے محفوظ ہو گیا ہے۔" } , status=status.HTTP_201_CREATED)
