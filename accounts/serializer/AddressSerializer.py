from rest_framework import serializers
# models imports
from accounts.model.Account import Address 
# Utils
from marble_erp.utils.langDetector import lang_detect
from marble_erp.utils.lang_translate import lang_translate

class AddressSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = Address
    fields = "__all__"
   




  def create(self, validate_data):  
    if "ADDRESS" in validate_data:          
      ADDRESS = validate_data["ADDRESS"]
      convertFrom, convertTo = lang_detect(ADDRESS)
      validate_data["ADDRESS"], validate_data["ADDRESS_UR"]  = lang_translate(stringToConvert=ADDRESS, from_lang=convertFrom, to_lang=convertTo)    
    if "TEHSIL" in validate_data:          
      TEHSIL = validate_data["TEHSIL"]
      convertFrom, convertTo = lang_detect(TEHSIL)
      validate_data["TEHSIL"], validate_data["TEHSIL_UR"]  = lang_translate(stringToConvert=TEHSIL, from_lang=convertFrom, to_lang=convertTo)
    if "PROVINCE" in validate_data:          
      PROVINCE = validate_data["PROVINCE"]
      convertFrom, convertTo = lang_detect(PROVINCE)
      validate_data["PROVINCE"], validate_data["PROVINCE_UR"]  = lang_translate(stringToConvert=PROVINCE, from_lang=convertFrom, to_lang=convertTo)
    if "POSTAL_CODE" in validate_data:          
      POSTAL_CODE = validate_data["POSTAL_CODE"]
      validate_data["POSTAL_CODE"], validate_data["POSTAL_CODE_UR"]  = lang_translate(stringToConvert=POSTAL_CODE, from_lang='en', to_lang='ur')
    
    if "CNTRY_NM" in validate_data:          
      CNTRY_NM = validate_data["CNTRY_NM"]
      convertFrom, convertTo = lang_detect(CNTRY_NM)
      validate_data["CNTRY_NM"], validate_data["CNTRY_NM_UR"]  = lang_translate(stringToConvert=CNTRY_NM, from_lang=convertFrom, to_lang=convertTo)
    
    address_created = Address.objects.create(**validate_data)
    return address_created
  

  
  def update(self, instance, validated_data):
    if "ADDRESS" in validated_data:          
      ADDRESS = validated_data["ADDRESS"]
      convertFrom, convertTo = lang_detect(ADDRESS)
      validated_data["ADDRESS"], validated_data["ADDRESS_UR"]  = lang_translate(stringToConvert=ADDRESS, from_lang=convertFrom, to_lang=convertTo)
    if "TEHSIL" in validated_data:          
      TEHSIL = validated_data["TEHSIL"]
      convertFrom, convertTo = lang_detect(TEHSIL)
      validated_data["TEHSIL"], validated_data["TEHSIL_UR"]  = lang_translate(stringToConvert=TEHSIL, from_lang=convertFrom, to_lang=convertTo)
    if "PROVINCE" in validated_data:          
      PROVINCE = validated_data["PROVINCE"]
      convertFrom, convertTo = lang_detect(PROVINCE)
      validated_data["PROVINCE"], validated_data["PROVINCE_UR"]  = lang_translate(stringToConvert=PROVINCE, from_lang=convertFrom, to_lang=convertTo)
    if "POSTAL_CODE" in validated_data:          
      POSTAL_CODE = validated_data["POSTAL_CODE"]
      validated_data["POSTAL_CODE"], validated_data["POSTAL_CODE_UR"]  = lang_translate(stringToConvert=POSTAL_CODE, from_lang='en', to_lang='ur')
    
    if "CNTRY_NM" in validated_data:          
      CNTRY_NM = validated_data["CNTRY_NM"]
      convertFrom, convertTo = lang_detect(CNTRY_NM)
      validated_data["CNTRY_NM"], validated_data["CNTRY_NM_UR"]  = lang_translate(stringToConvert=CNTRY_NM, from_lang=convertFrom, to_lang=convertTo)
  
        
    instance.IS_PRIMARY = validated_data.get('IS_PRIMARY', instance.IS_PRIMARY)
    instance.ADDRESS = validated_data.get('ADDRESS', instance.ADDRESS)
    instance.ADDRESS_UR = validated_data.get('ADDRESS_UR', instance.ADDRESS_UR)
    instance.TEHSIL = validated_data.get('TEHSIL', instance.TEHSIL)
    instance.TEHSIL_UR = validated_data.get('TEHSIL_UR', instance.TEHSIL_UR)
    instance.PROVINCE = validated_data.get('PROVINCE', instance.PROVINCE)
    instance.PROVINCE_UR = validated_data.get('PROVINCE_UR', instance.PROVINCE_UR)
    instance.CNTRY_NM = validated_data.get('CNTRY_NM', instance.CNTRY_NM)
    instance.CNTRY_NM_UR = validated_data.get('CNTRY_NM_UR', instance.CNTRY_NM_UR)
    instance.POSTAL_CODE = validated_data.get('POSTAL_CODE', instance.POSTAL_CODE)
    instance.POSTAL_CODE_UR = validated_data.get('POSTAL_CODE_UR', instance.POSTAL_CODE_UR)
    instance.DNM = validated_data.get('DNM', instance.DNM)
    instance.CNTRY_ABB = validated_data.get('CNTRY_ABB', instance.CNTRY_ABB)
    instance.save()
        
    return instance
