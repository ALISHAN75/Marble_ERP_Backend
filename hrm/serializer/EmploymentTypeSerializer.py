from rest_framework import serializers
from hrm.model.Employment_Types import Employment_Types
from marble_erp.utils.langDetector import lang_detect
from marble_erp.utils.lang_translate import lang_translate


class EmploymentTypeSerializer(serializers.ModelSerializer):
   
  class Meta:
    model = Employment_Types
    fields = "__all__"
    

  def create(self, validate_data):
        if "EMP_TYP_NM" in validate_data:          
            EMP_TYP_NM = validate_data.get('EMP_TYP_NM')
            convertFrom, convertTo = lang_detect(EMP_TYP_NM)
            validate_data["EMP_TYP_NM"], validate_data["EMP_TYP_NM_UR"]  = lang_translate(stringToConvert=EMP_TYP_NM, from_lang=convertFrom, to_lang=convertTo)
            
        if "EMP_TYP_DESC" in validate_data:          
            EMP_TYP_DESC = validate_data.get('EMP_TYP_DESC')
            convertFrom, convertTo = lang_detect(EMP_TYP_DESC)
            validate_data["EMP_TYP_DESC"], validate_data["EMP_TYP_DESC_UR"]  = lang_translate(stringToConvert=EMP_TYP_DESC, from_lang=convertFrom, to_lang=convertTo)

  
        return Employment_Types.objects.create(**validate_data)

  def update(self, instance, validated_data):
        if "EMP_TYP_NM" in validated_data:          
            EMP_TYP_NM = validated_data.get('EMP_TYP_NM')
            convertFrom, convertTo = lang_detect(EMP_TYP_NM)
            validated_data["EMP_TYP_NM"], validated_data["EMP_TYP_NM_UR"]  = lang_translate(stringToConvert=EMP_TYP_NM, from_lang=convertFrom, to_lang=convertTo)
        
        if "EMP_TYP_DESC" in validated_data:          
            EMP_TYP_DESC = validated_data.get('EMP_TYP_DESC')
            convertFrom, convertTo = lang_detect(EMP_TYP_DESC)
            validated_data["EMP_TYP_DESC"], validated_data["EMP_TYP_DESC_UR"]  = lang_translate(stringToConvert=EMP_TYP_DESC, from_lang=convertFrom, to_lang=convertTo)

        instance.EMP_TYP_NM = validated_data.get('EMP_TYP_NM', instance.EMP_TYP_NM)
        instance.EMP_TYP_NM_UR = validated_data.get('EMP_TYP_NM_UR', instance.EMP_TYP_NM_UR)
        instance.EMP_TYP_DESC = validated_data.get('EMP_TYP_DESC', instance.EMP_TYP_DESC)
        instance.EMP_TYP_DESC_UR = validated_data.get('EMP_TYP_DESC_UR', instance.EMP_TYP_DESC_UR)

        instance.save()
        return instance
