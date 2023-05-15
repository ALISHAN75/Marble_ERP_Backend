from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
# models imports
from accounts.model.Account import Accounts, User
# models imports
from hrm.model.Employee import Employee, Employee_Compensation
# serializers import
from accounts.serializer.UsersSerializer import UserProfileSerializer, AccountsSerializer
from hrm.serializer.DesignationSerializer import DesignationSerializer
from hrm.serializer.EmploymentTypeSerializer import EmploymentTypeSerializer
from hrm.serializer.EmployeeCompensationSerializer import EmployeeCompensationSerializer
from marble_erp.utils.langDetector import lang_detect
from marble_erp.utils.lang_translate import lang_translate
from accounts.serializer.UsersSerializer import UserRegistrationSerializer  , UserDetailSerializer
from accounts.serializer.AddressSerializer import AddressSerializer
from accounts.serializer.PhNumberSerializer import PhNumberSerializer
from accounts.serializer.AccountTypeSerializer import AccountTypeSerializer



class EmployeeSerializer(serializers.ModelSerializer):
    USER = UserRegistrationSerializer()
    EMP_COMPENSATION = EmployeeCompensationSerializer(many=True)
    class Meta:
        model = Employee
        fields = "__all__"
        
     
    def create(self, validate_data):
        USER = validate_data.pop('USER' , {})
        emp_cmpnstion = validate_data.pop("EMP_COMPENSATION", [])
        if "EMP_TERM_REASN" in validate_data and len(validate_data["EMP_TERM_REASN"])>0:          
            EMP_TERM_REASN = validate_data.get('EMP_TERM_REASN')
            convertFrom, convertTo = lang_detect(EMP_TERM_REASN)
            validate_data["EMP_TERM_REASN"], validate_data["EMP_TERM_REASN_UR"]  = lang_translate(stringToConvert=EMP_TERM_REASN, from_lang=convertFrom, to_lang=convertTo)
        if "EMP_FULL_NM" in validate_data and len(validate_data["EMP_FULL_NM"])>0:          
            EMP_FULL_NM = validate_data.get('EMP_FULL_NM')
            convertFrom, convertTo = lang_detect(EMP_FULL_NM)
            validate_data["EMP_FULL_NM"], validate_data["EMP_FULL_NM_UR"]  = lang_translate(stringToConvert=EMP_FULL_NM, from_lang=convertFrom, to_lang=convertTo)        
        create_serializer = UserRegistrationSerializer(data=USER)
        if create_serializer.is_valid():
            new_user = create_serializer.save()
        validate_data["USER_ID"] = new_user
        created_employee = Employee.objects.create(**validate_data)

        
        return created_employee

    def update(self, instance, validated_data):
        USER = validated_data.pop('USER' , {})
        emp_cmpnstion = validated_data.pop("EMP_COMPENSATION" , [])
        if "EMP_TERM_REASN" in validated_data  and len(validated_data["EMP_TERM_REASN"])>0:          
            EMP_TERM_REASN = validated_data.get('EMP_TERM_REASN')
            convertFrom, convertTo = lang_detect(EMP_TERM_REASN)
            validated_data["EMP_TERM_REASN"], validated_data["EMP_TERM_REASN_UR"]  = lang_translate(stringToConvert=EMP_TERM_REASN, from_lang=convertFrom, to_lang=convertTo)
        if "EMP_FULL_NM" in validated_data and len(validated_data["EMP_FULL_NM"])>0:          
            EMP_FULL_NM = validated_data.get('EMP_FULL_NM')
            convertFrom, convertTo = lang_detect(EMP_FULL_NM)
            validated_data["EMP_FULL_NM"], validated_data["EMP_FULL_NM_UR"]  = lang_translate(stringToConvert=EMP_FULL_NM, from_lang=convertFrom, to_lang=convertTo)  

        instance.EMP_FULL_NM = validated_data.get('EMP_FULL_NM', instance.EMP_FULL_NM)
        instance.EMP_FULL_NM_UR = validated_data.get('EMP_FULL_NM_UR', instance.EMP_FULL_NM_UR)
        instance.EMP_STRT_DT = validated_data.get('EMP_STRT_DT', instance.EMP_STRT_DT)
        instance.EMP_TERM_DT = validated_data.get('EMP_TERM_DT', instance.EMP_TERM_DT)
        instance.EMP_STS = validated_data.get('EMP_STS', instance.EMP_STS)
        instance.EMP_TERM_REASN = validated_data.get('EMP_TERM_REASN', instance.EMP_TERM_REASN)
        instance.EMP_TERM_REASN_UR = validated_data.get('EMP_TERM_REASN_UR', instance.EMP_TERM_REASN_UR)
        instance.CNIC = validated_data.get('CNIC', instance.CNIC)
        instance.CNIC_EXP_DT = validated_data.get('CNIC_EXP_DT', instance.CNIC_EXP_DT)
        instance.IS_ACTIVE = validated_data.get('IS_ACTIVE', instance.IS_ACTIVE)
        instance.REC_ADD_BY = validated_data.get('REC_ADD_BY', instance.REC_ADD_BY)
        instance.REC_MOD_BY = validated_data.get('REC_MOD_BY', instance.REC_MOD_BY)
        instance.REC_MOD_DT = validated_data.get('REC_MOD_DT', instance.REC_MOD_DT)
        instance.REC_ADD_DT = validated_data.get('REC_ADD_DT', instance.REC_ADD_DT)
        instance.EMP_DESIG_ID = validated_data.get('EMP_DESIG_ID', instance.EMP_DESIG_ID)
        instance.EMP_TYP_ID = validated_data.get('EMP_TYP_ID', instance.EMP_TYP_ID)
        instance.save()

        
        # unique_words = "11b1b1b1b1b"
        # try:        
        #     acc_to_update = User.objects.get(email=instance.USER_ID)
        #     acc_to_update.email = USER['email'].replace(unique_words, '')
        #     acc_to_update.save()
        # except User.DoesNotExist:
        #     return Response({'error': 'The User does not exist.'  , "error_ur" : "صارف موجود نہیں ہے۔"  }, status=status.HTTP_400_BAD_REQUEST)
        # update_serializer = UserRegistrationSerializer(instance=acc_to_update , data=USER )
        # if update_serializer.is_valid():
        #     updated_account = update_serializer.save()
        #     validated_data["USER_ID"] = updated_account
        #     instance.USER_ID = validated_data.get('USER_ID', instance.USER_ID)
        #     instance.save()

        


        return instance


