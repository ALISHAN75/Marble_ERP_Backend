from audioop import add
import django
from rest_framework import serializers
from accounts.model.Account import Accounts, User, Phone_Numbers  , acct_id_type_id_link, Address , account_type
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.models import Group
from accounts.utils import Util
from rest_framework import status
from rest_framework.response import Response
# serializers
from accounts.serializer.AddressSerializer import AddressSerializer
from accounts.serializer.PhNumberSerializer import PhNumberSerializer
from accounts.serializer.AccountTypeSerializer import AccountTypeSerializer
# Utils
from marble_erp.utils.langDetector import lang_detect
from marble_erp.utils.lang_translate import lang_translate


class UserSerializer(serializers.ModelSerializer):
  address_info = AddressSerializer(many=True)
  contact_info = PhNumberSerializer(many=True)

  class Meta:
    model = User
    fields=  (
      'id',
      'email',
      'FIRST_NAME',
      'LAST_NAME',
      'is_superuser',
      'is_admin',
      'is_active',
      'address_info',
      'contact_info',
      'groups',
      'user_permissions'
    )



class AccountsDetailSerializer(serializers.ModelSerializer):
  # ACCT_TYPE_ID = AccountsTypeSerializer(many=True)
  class Meta:
    model = Accounts
    fields = '__all__'
    depth = 1



class AccountsSerializer(serializers.ModelSerializer):
  ACCT_TYPE_ID = serializers.ListField(child = serializers.IntegerField())
  class Meta:
    model = Accounts
    fields = '__all__'


class AddAccountsSerializer(serializers.ModelSerializer):
  ACCT_TYPE_ID = serializers.ListField(child = serializers.IntegerField())
  class Meta:
    model = Accounts
    fields = '__all__'

  def create(self, validate_data):
    acct_type_ids = validate_data["ACCT_TYPE_ID"]
    validate_data["CLOSNG_BLNCE"] = validate_data["OPNG_BLNCE"]
    if "ACCT_TITLE" in validate_data:          
            ACCT_TITLE = validate_data["ACCT_TITLE"]
            convertFrom, convertTo = lang_detect(ACCT_TITLE)
            validate_data["ACCT_TITLE"], validate_data["ACCT_TITLE_UR"]  = lang_translate(stringToConvert=ACCT_TITLE, from_lang=convertFrom, to_lang=convertTo)
    if "ACCT_REF" in validate_data:          
            ACCT_REF = validate_data["ACCT_REF"]
            convertFrom, convertTo = lang_detect(ACCT_REF)
            validate_data["ACCT_REF"], validate_data["ACCT_REF_UR"]  = lang_translate(stringToConvert=ACCT_REF, from_lang=convertFrom, to_lang=convertTo)
    if "ACCT_DESC" in validate_data:          
            ACCT_DESC = validate_data["ACCT_DESC"]
            convertFrom, convertTo = lang_detect(ACCT_DESC)
            validate_data["ACCT_DESC"], validate_data["ACCT_DESC_UR"]  = lang_translate(stringToConvert=ACCT_DESC, from_lang=convertFrom, to_lang=convertTo)

    validate_data.pop("ACCT_TYPE_ID")
    new_acct = Accounts.objects.create(**validate_data)

    # add acct_type_ids
    for acct_link in acct_type_ids:
      acct_type = account_type.objects.get(ACCT_TYPE_ID=acct_link)
      new_acct.acct_type.add(acct_type)
 
    return new_acct

  def update(self, instance, validated_data):
    if "ACCT_TITLE" in validated_data:         
        ACCT_TITLE = validated_data["ACCT_TITLE"]
        convertFrom, convertTo = lang_detect(ACCT_TITLE)
        validated_data["ACCT_TITLE"], validated_data["ACCT_TITLE_UR"]  = lang_translate(stringToConvert=ACCT_TITLE, from_lang=convertFrom, to_lang=convertTo)
    if "ACCT_REF" in validated_data:          
          ACCT_REF = validated_data["ACCT_REF"]
          convertFrom, convertTo = lang_detect(ACCT_REF)
          validated_data["ACCT_REF"], validated_data["ACCT_REF_UR"]  = lang_translate(stringToConvert=ACCT_REF, from_lang=convertFrom, to_lang=convertTo)
    if "ACCT_DESC" in validated_data:          
          ACCT_DESC = validated_data["ACCT_DESC"]
          convertFrom, convertTo = lang_detect(ACCT_DESC)
          validated_data["ACCT_DESC"], validated_data["ACCT_DESC_UR"]  = lang_translate(stringToConvert=ACCT_DESC, from_lang=convertFrom, to_lang=convertTo)
  

    instance.ACCT_TITLE = validated_data.get('ACCT_TITLE', instance.ACCT_TITLE)
    instance.ACCT_TITLE_UR = validated_data.get('ACCT_TITLE_UR', instance.ACCT_TITLE_UR)
    instance.ACCT_REF = validated_data.get('ACCT_REF', instance.ACCT_REF)
    instance.ACCT_REF = validated_data.get('ACCT_REF_UR', instance.ACCT_REF_UR)
    instance.ACCT_DESC = validated_data.get('ACCT_DESC', instance.ACCT_DESC)
    instance.ACCT_DESC_UR = validated_data.get('ACCT_DESC_UR', instance.ACCT_DESC_UR)

    instance.ACCT_TYP = validated_data.get('ACCT_TYP', instance.ACCT_TYP)
    instance.IS_ACTIVE = validated_data.get('IS_ACTIVE', instance.IS_ACTIVE)
    instance.OPNG_BLNCE = validated_data.get('OPNG_BLNCE', instance.OPNG_BLNCE)
    instance.CLOSNG_BLNCE = validated_data.get('CLOSNG_BLNCE', instance.CLOSNG_BLNCE)
    instance.ACCT_CREATE_DT = validated_data.get('ACCT_CREATE_DT', instance.ACCT_CREATE_DT)
    instance.REC_ADD_BY = validated_data.get('REC_ADD_BY', instance.REC_ADD_BY)
    instance.REC_MOD_BY = validated_data.get('REC_MOD_BY', instance.REC_MOD_BY)
    instance.REC_MOD_DT = validated_data.get('REC_MOD_DT', instance.REC_MOD_DT)
    instance.REC_ADD_DT = validated_data.get('REC_ADD_DT', instance.REC_ADD_DT)
    instance.save()  

    return instance




class AccountDetailSerializer(serializers.ModelSerializer):
  account = AccountsDetailSerializer(many=True)
  addresses = AddressSerializer(many=True)
  contact_info = PhNumberSerializer(many=True)
  class Meta:
    model = Accounts
    fields = "__all__"
    depth = 1

class UserDetailExtraSerializer(serializers.ModelSerializer):
  addresses = AddressSerializer(many=True)
  contact_info = PhNumberSerializer(many=True)
  class Meta:
    model = User
    fields = "__all__"
    # depth = 2

class AccountsDetailExtraSerializer(serializers.ModelSerializer):
  # ACCT_TYPE_ID = AccountsTypeSerializer(many=True)
  address_info = AddressSerializer(many=True)
  contact_info = PhNumberSerializer(many=True)
  class Meta:
    model = Accounts
    fields = '__all__'
    depth = 1

  
class UserDetailSerializer(serializers.ModelSerializer):
  account = AccountsDetailSerializer()
  addresses = AddressSerializer(many=True)
  contact_info = PhNumberSerializer(many=True)
  # roles = serializers.ListField(child = serializers.IntegerField())

  class Meta:
    model = User
    fields = "__all__"
    depth = 2

class UserRegistrationSerializer(serializers.ModelSerializer):
  account = AccountsSerializer()
  addresses = AddressSerializer(many=True)
  contact_info = PhNumberSerializer(many=True)

  # We are writing this becoz we need confirm password field in our Registratin Request roles and permissions
  confirm_password = serializers.CharField(style={'input_type':'password'}, write_only=True)
  roles = serializers.ListField(child = serializers.IntegerField())

  class Meta:
    model = User
    fields = "__all__"   
    extra_kwargs={
      'password':{'write_only':True}
    }



  def validate(self, attrs):
    password = attrs.get('password')
    confirm_password = attrs.get('confirm_password')
    contact_info = attrs.get("contact_info")
    nmbr=0
    if password != confirm_password:
      raise serializers.ValidationError({'error': "Password and Confirm Password doesn't match" , 'error_ur': 'پاس ورڈ اور کنفرم پاس ورڈ مماثل نہیں ہیں۔' } ) 
    return attrs

  def create(self, validate_data):
    new_acct = 0
    acct_type_ids = []
    ph_check = True 
    addrs_check = True 
    addresses = validate_data.pop('addresses')
    contact_info = validate_data.pop("contact_info")
    roles = validate_data.pop("roles")
    acct = validate_data.pop("account")
    FIRST_NAME = validate_data.get('FIRST_NAME')
    LAST_NAME = validate_data.get('LAST_NAME')
    user_id = validate_data.get('REC_ADD_BY')
    if FIRST_NAME:         
        convertFrom, convertTo = lang_detect(FIRST_NAME)
        validate_data["FIRST_NAME"], validate_data["FIRST_NAME_UR"]  = lang_translate(stringToConvert=FIRST_NAME, from_lang=convertFrom, to_lang=convertTo)
    if not FIRST_NAME:
      validate_data["FIRST_NAME_UR"] = None

    if "LAST_NAME" in validate_data:
      convertFrom, convertTo = lang_detect(LAST_NAME)
      validate_data["LAST_NAME"], validate_data["LAST_NAME_UR"]  = lang_translate(stringToConvert=LAST_NAME, from_lang=convertFrom, to_lang=convertTo)
    created_user = User.objects.create_user(**validate_data)   

    acct_type_ids = acct["ACCT_TYPE_ID"]
    acct["REC_ADD_BY"] = user_id
    acct["REC_MOD_BY"] = user_id
    acct["USER_ID"] = created_user
    acct["CLOSNG_BLNCE"] = acct["OPNG_BLNCE"]
    if "ACCT_TITLE" in acct:          
            ACCT_TITLE = acct["ACCT_TITLE"]
            convertFrom, convertTo = lang_detect(ACCT_TITLE)
            acct["ACCT_TITLE"], acct["ACCT_TITLE_UR"]  = lang_translate(stringToConvert=ACCT_TITLE, from_lang=convertFrom, to_lang=convertTo)
    if "ACCT_REF" in acct:          
            ACCT_REF = acct["ACCT_REF"]
            convertFrom, convertTo = lang_detect(ACCT_REF)
            acct["ACCT_REF"], acct["ACCT_REF_UR"]  = lang_translate(stringToConvert=ACCT_REF, from_lang=convertFrom, to_lang=convertTo)
    if "ACCT_DESC" in acct:          
            ACCT_DESC = acct["ACCT_DESC"]
            convertFrom, convertTo = lang_detect(ACCT_DESC)
            acct["ACCT_DESC"], acct["ACCT_DESC_UR"]  = lang_translate(stringToConvert=ACCT_DESC, from_lang=convertFrom, to_lang=convertTo)
    acct.pop("ACCT_TYPE_ID")
    new_acct = Accounts.objects.create(**acct)


    # add address info
    for addr in  addresses:
      addr["USER"] = created_user
      if "ADDRESS" in addr:          
            ADDRESS = addr["ADDRESS"]
            convertFrom, convertTo = lang_detect(ADDRESS)
            addr["ADDRESS"], addr["ADDRESS_UR"]  = lang_translate(stringToConvert=ADDRESS, from_lang=convertFrom, to_lang=convertTo)
      if "TEHSIL" in addr:          
            TEHSIL = addr["TEHSIL"]
            convertFrom, convertTo = lang_detect(TEHSIL)
            addr["TEHSIL"], addr["TEHSIL_UR"]  = lang_translate(stringToConvert=TEHSIL, from_lang=convertFrom, to_lang=convertTo)
      if "PROVINCE" in addr:          
            PROVINCE = addr["PROVINCE"]
            convertFrom, convertTo = lang_detect(PROVINCE)
            addr["PROVINCE"], addr["PROVINCE_UR"]  = lang_translate(stringToConvert=PROVINCE, from_lang=convertFrom, to_lang=convertTo)
      if "POSTAL_CODE" in addr:          
            POSTAL_CODE = addr["POSTAL_CODE"]
            addr["POSTAL_CODE"], addr["POSTAL_CODE_UR"]  = lang_translate(stringToConvert=POSTAL_CODE, from_lang='en', to_lang='ur')    
      if "CNTRY_NM" in addr:          
            CNTRY_NM = addr["CNTRY_NM"]
            convertFrom, convertTo = lang_detect(CNTRY_NM)
            addr["CNTRY_NM"], addr["CNTRY_NM_UR"]  = lang_translate(stringToConvert=CNTRY_NM, from_lang=convertFrom, to_lang=convertTo)    
      
      
      if addrs_check is True :
        addr["IS_PRIMARY"] = 1
        addrs_check = False
      Address.objects.create(**addr)


    # Check for user with same phone numbers couldn't be add into DB
    for ph in  contact_info:
      nmbr = ph["PH_NUM"]
      try:
        same_nmbr = Phone_Numbers.objects.get(IS_PRIMARY=1,PH_NUM=nmbr)
        raise serializers.ValidationError({'error': "User with this phone number already exists." , 'error_ur': 'اس فون نمبر والا صارف پہلے سے موجود ہے۔"' } )
      except Phone_Numbers.DoesNotExist:
        pass

    for ph in  contact_info:
      ph["USER"] = created_user
      if ph_check is True :
        ph["IS_PRIMARY"] = 1
        ph_check = False
      Phone_Numbers.objects.create(**ph)

     # add role
    for role in roles:
     role = Group.objects.get(id=role)
     created_user.groups.add(role) 


    # add acct_type_ids
    for acct_link in acct_type_ids:
      acct_type = account_type.objects.get(ACCT_TYPE_ID=acct_link)
      new_acct.acct_type.add(acct_type)
    return created_user

  
  def update(self, instance, validated_data):
    acct =  validated_data.pop("account", {})
    user_roles =  validated_data.pop("roles", [])
    roles = validated_data.pop("roles" , [])
    user_addresses =  validated_data.pop("addresses", [])
    user_contact_info =  validated_data.pop("contact_info", [])
    if "LAST_NAME" in validated_data:          
      LAST_NAME =  validated_data.pop("LAST_NAME")
      convertFrom, convertTo = lang_detect(LAST_NAME)
      validated_data["LAST_NAME"], validated_data["LAST_NAME_UR"]  = lang_translate(stringToConvert= LAST_NAME, from_lang=convertFrom, to_lang=convertTo)
    if "FIRST_NAME" in validated_data:
      FIRST_NAME =  validated_data.pop("FIRST_NAME")
      if FIRST_NAME:         
        convertFrom, convertTo = lang_detect(FIRST_NAME)
        validated_data["FIRST_NAME"], validated_data["FIRST_NAME_UR"]  = lang_translate(stringToConvert=FIRST_NAME, from_lang=convertFrom, to_lang=convertTo)
    if not FIRST_NAME:
      validated_data["FIRST_NAME_UR"] = None
     
    acct_type_ids = acct["ACCT_TYPE_ID"]
    # Update User
    unique_words = "11b1b1b1b1b"
    validated_data["email"] =  validated_data.get('email').replace(unique_words, '')
    instance.email = validated_data.get('email', instance.email)
    instance.FIRST_NAME = validated_data.get('FIRST_NAME', instance.FIRST_NAME)
    instance.FIRST_NAME_UR = validated_data.get('FIRST_NAME_UR', instance.FIRST_NAME_UR)
    instance.LAST_NAME = validated_data.get('LAST_NAME', instance.LAST_NAME)
    instance.LAST_NAME_UR = validated_data.get('LAST_NAME_UR', instance.LAST_NAME_UR)
    # instance.password = validated_data.get('password', instance.password)
    instance.REC_ADD_BY = validated_data.get('REC_ADD_BY', instance.REC_ADD_BY)
    instance.REC_MOD_BY = validated_data.get('REC_MOD_BY', instance.REC_MOD_BY)
    instance.save()

    # for acct in user_account:
    if "ACCT_TITLE" in acct:         
        ACCT_TITLE = acct["ACCT_TITLE"]
        convertFrom, convertTo = lang_detect(ACCT_TITLE)
        acct["ACCT_TITLE"], acct["ACCT_TITLE_UR"]  = lang_translate(stringToConvert=ACCT_TITLE, from_lang=convertFrom, to_lang=convertTo)
    if "ACCT_REF" in acct:          
          ACCT_REF = acct["ACCT_REF"]
          convertFrom, convertTo = lang_detect(ACCT_REF)
          acct["ACCT_REF"], acct["ACCT_REF_UR"]  = lang_translate(stringToConvert=ACCT_REF, from_lang=convertFrom, to_lang=convertTo)
    if "ACCT_DESC" in acct:          
          ACCT_DESC = acct["ACCT_DESC"]
          convertFrom, convertTo = lang_detect(ACCT_DESC)
          acct["ACCT_DESC"], acct["ACCT_DESC_UR"]  = lang_translate(stringToConvert=ACCT_DESC, from_lang=convertFrom, to_lang=convertTo)
      
    account =  Accounts.objects.get(USER_ID=instance.id)
    account.USER_ID = instance
    account.ACCT_TITLE = acct.get('ACCT_TITLE', account.ACCT_TITLE)
    account.ACCT_TITLE_UR = acct.get('ACCT_TITLE_UR', account.ACCT_TITLE_UR)
    account.ACCT_REF = acct.get('ACCT_REF', account.ACCT_REF)
    account.ACCT_REF_UR = acct.get('ACCT_REF_UR', account.ACCT_REF_UR)
    account.ACCT_DESC = acct.get('ACCT_DESC', account.ACCT_DESC)
    account.ACCT_DESC_UR = acct.get('ACCT_DESC_UR', account.ACCT_DESC_UR)

    account.ACCT_TYP = acct.get('ACCT_TYP', account.ACCT_TYP)
    account.IS_ACTIVE = acct.get('IS_ACTIVE', account.IS_ACTIVE)
    account.OPNG_BLNCE = acct.get('OPNG_BLNCE', account.OPNG_BLNCE)
    account.CLOSNG_BLNCE = acct.get('CLOSNG_BLNCE', account.CLOSNG_BLNCE)
    account.ACCT_CREATE_DT = acct.get('ACCT_CREATE_DT', account.ACCT_CREATE_DT)
    account.REC_ADD_BY = acct.get('REC_ADD_BY', account.REC_ADD_BY)
    account.REC_MOD_BY = acct.get('REC_MOD_BY', account.REC_MOD_BY)
    account.REC_MOD_DT = acct.get('REC_MOD_DT', account.REC_MOD_DT)
    account.REC_ADD_DT = acct.get('REC_ADD_DT', account.REC_ADD_DT)
    new_acct =  account.save()


    
    # Delete Previous roles
    instance.groups.clear()
    # Add Roles
    for role in user_roles:
      role = Group.objects.get(id=role)
      instance.groups.add(role)

    # Delete account data from Middle table then add new data 
    account.acct_type.clear()
    # add acct_type_ids
    for acct_link in acct_type_ids:
      acct_type = account_type.objects.get(ACCT_TYPE_ID=acct_link)
      acct_type_delete = account.acct_type.filter(accounts = account)
      account.acct_type.add(acct_type)
    return instance


class UserLoginSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    model = User
    fields = ['email', 'password']


class UserProfileSerializer(serializers.ModelSerializer):
  # permissions =  PermissionSerializer(many=True, source='user_permissions')
  address_info = AddressSerializer(many=True, read_only=True)
  contact_info = PhNumberSerializer(many=True, read_only=True)

  class Meta:
    model = User
    fields=  (
      'id',
      'email',
      'FIRST_NAME',
      'LAST_NAME',
      'is_superuser',
      'is_admin',
      'is_active',
      'address_info',
      'contact_info',
      'groups',
      'user_permissions'
    )


class UserChangePasswordSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  confirm_password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'confirm_password']

  def validate(self, attrs):
    password = attrs.get('password')
    confirm_password = attrs.get('confirm_password')
    user = self.context.get('user')
    if password != confirm_password:
      raise serializers.ValidationError({'error': "Password and Confirm Password doesn't match" , 'error_ur': 'پاس ورڈ اور کنفرم پاس ورڈ مماثل نہیں ہیں۔' } ) 
    user.set_password(password)
    user.save()
    return attrs


class SendPasswordResetEmailSerializer(serializers.Serializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    fields = ['email']

  def validate(self, attrs):
    email = attrs.get('email')
    if User.objects.filter(email=email).exists():
      user = User.objects.get(email = email)
      uid = urlsafe_base64_encode(force_bytes(user.id))
      token = PasswordResetTokenGenerator().make_token(user)
      link = 'http://localhost:3000/api/user/reset/'+uid+'/'+token
      # Send EMail
      body = 'Click Following Link to Reset Your Password '+link
      data = {
        'subject':'Reset Your Password',
        'body':body,
        'to_email':user.email
      }
      # Util.send_email(data)
      return attrs
    else:
      raise  serializers.ValidationError({'error': "You are not a registered user" , 'error_ur': 'آپ رجسٹرڈ صارف نہیں ہیں۔' } ) 
      


class UserPasswordResetSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  confirm_password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'confirm_password']

  def validate(self, attrs):
    try:
      password = attrs.get('password')
      confirm_password = attrs.get('confirm_password')
      uid = self.context.get('uid')
      token = self.context.get('token')
      if password != confirm_password:
        raise  serializers.ValidationError({'error': "Password and Confirm Password doesn't match" , 'error_ur': 'پاس ورڈ اور کنفرم پاس ورڈ مماثل نہیں ہیں۔' } ) 
      id = smart_str(urlsafe_base64_decode(uid))
      user = User.objects.get(id=id)
      if not PasswordResetTokenGenerator().check_token(user, token):
        raise   serializers.ValidationError({'error': "Token is not valid or it is expired'" , 'error_ur': 'ٹوکن درست نہیں ہے یا اس کی میعاد ختم ہو چکی ہے' } )
      user.set_password(password)
      user.save()
      return attrs
    except DjangoUnicodeDecodeError as identifier:
      PasswordResetTokenGenerator().check_token(user, token)
      raise  serializers.ValidationError({'error': "Token is not valid or it is expired'" , 'error_ur': 'ٹوکن درست نہیں ہے یا اس کی میعاد ختم ہو چکی ہے' } ) 




  

    
