from rest_framework import serializers
# models imports
from hrm.model.Employee import Employee_Compensation
from marble_erp.utils.langDetector import lang_detect
from marble_erp.utils.lang_translate import lang_translate

class EmployeeCompensationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee_Compensation
        fields = "__all__"
        
    
    def create(self, validate_data):
        if "COMPNSTN_UNIT" in validate_data and len(validate_data["COMPNSTN_UNIT"])>0 and validate_data["COMPNSTN_UNIT"] is not None:         
            COMPNSTN_UNIT = validate_data.get('COMPNSTN_UNIT')
            convertFrom, convertTo = lang_detect(COMPNSTN_UNIT)
            validate_data["COMPNSTN_UNIT"], validate_data["COMPNSTN_UNIT_UR"]  = lang_translate(stringToConvert=COMPNSTN_UNIT, from_lang=convertFrom, to_lang=convertTo)      
        if "PAY_FREQ_TYP" in validate_data  and len(validate_data["PAY_FREQ_TYP"])>0  and validate_data["PAY_FREQ_TYP"] is not None:            
            PAY_FREQ_TYP = validate_data.get('PAY_FREQ_TYP')
            convertFrom, convertTo = lang_detect(PAY_FREQ_TYP)
            validate_data["PAY_FREQ_TYP"], validate_data["PAY_FREQ_TYP_UR"]  = lang_translate(stringToConvert=PAY_FREQ_TYP, from_lang=convertFrom, to_lang=convertTo)
        return Employee_Compensation.objects.create(**validate_data)

    def update(self, instance, validated_data):
        if "COMPNSTN_UNIT" in validated_data  and validated_data["COMPNSTN_UNIT"] is not None:          
            COMPNSTN_UNIT = validated_data.get('COMPNSTN_UNIT')
            convertFrom, convertTo = lang_detect(COMPNSTN_UNIT)
            validated_data["COMPNSTN_UNIT"], validated_data["COMPNSTN_UNIT_UR"]  = lang_translate(stringToConvert=COMPNSTN_UNIT, from_lang=convertFrom, to_lang=convertTo)      
        if "PAY_FREQ_TYP" in validated_data  and validated_data["PAY_FREQ_TYP"] is not None:            
            PAY_FREQ_TYP = validated_data.get('PAY_FREQ_TYP')
            convertFrom, convertTo = lang_detect(PAY_FREQ_TYP)
            validated_data["PAY_FREQ_TYP"], validated_data["PAY_FREQ_TYP_UR"]  = lang_translate(stringToConvert=PAY_FREQ_TYP, from_lang=convertFrom, to_lang=convertTo)

        instance.COMPNSTN_AMNT = validated_data.get('COMPNSTN_AMNT', instance.COMPNSTN_AMNT)
        instance.COMPNSTN_UNIT = validated_data.get('COMPNSTN_UNIT', instance.COMPNSTN_UNIT)
        instance.COMPNSTN_UNIT_UR = validated_data.get('COMPNSTN_UNIT_UR', instance.COMPNSTN_UNIT_UR)
        instance.PAY_FREQ_TYP = validated_data.get('PAY_FREQ_TYP', instance.PAY_FREQ_TYP)
        instance.PAY_FREQ_TYP_UR = validated_data.get('PAY_FREQ_TYP_UR', instance.PAY_FREQ_TYP_UR)
        instance.EFFCT_STRT_DT = validated_data.get('EFFCT_STRT_DT', instance.EFFCT_STRT_DT)
        instance.EFFCT_END_DT = validated_data.get('EFFCT_END_DT', instance.EFFCT_END_DT)
        instance.REC_ADD_BY = validated_data.get('REC_ADD_BY', instance.REC_ADD_BY)
        instance.REC_MOD_BY = validated_data.get('REC_MOD_BY', instance.REC_MOD_BY)
        instance.REC_MOD_DT = validated_data.get('REC_MOD_DT', instance.REC_MOD_DT)
        instance.REC_ADD_DT = validated_data.get('REC_ADD_DT', instance.REC_ADD_DT)
        instance.EMP_ID = validated_data.get('EMP_ID', instance.EMP_ID)
        instance.save()
        return instance

