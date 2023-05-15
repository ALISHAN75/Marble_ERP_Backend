from rest_framework import serializers
# models imports
from hrm.model.Employee_Designations import Employee_Designations
# serializers import
from hrm.serializer.DepartmentsSerializer import DepartmentsSerializer
from marble_erp.utils.langDetector import lang_detect
from marble_erp.utils.lang_translate import lang_translate

class DesignationSerializer(serializers.ModelSerializer):

    EMP_DEPT = DepartmentsSerializer(read_only=True)

    class Meta:
        model = Employee_Designations
        fields = (
            'EMP_DESIG_ID',
            'DESIG_NM',
            'DESIG_NM_UR',
            'DESIG_DESC',
            'DESIG_DESC_UR',
            'EMP_DEPT_ID',
            'EMP_DEPT',
            'IS_ACTIVE',
            'REC_ADD_DT',
            'REC_ADD_BY',
            'REC_MOD_DT',
            'REC_MOD_BY'
        )

    def create(self, validate_data):
        if "DESIG_NM" in validate_data and  len(validate_data["DESIG_NM"])>0:          
            design_name = validate_data.get('DESIG_NM')
            convertFrom, convertTo = lang_detect(design_name)
            validate_data["DESIG_NM"], validate_data["DESIG_NM_UR"]  = lang_translate(stringToConvert=design_name, from_lang=convertFrom, to_lang=convertTo)
        
        if "DESIG_DESC" in validate_data  and  len(validate_data["DESIG_DESC"])>0:          
            design_desc = validate_data.get('DESIG_DESC', None)
            convertFrom, convertTo = lang_detect(design_desc)
            validate_data["DESIG_DESC"], validate_data["DESIG_DESC_UR"]  = lang_translate(stringToConvert=design_desc, from_lang=convertFrom, to_lang=convertTo)

        return Employee_Designations.objects.create(**validate_data)

    def update(self, instance, validated_data):
        if "DESIG_NM" in validated_data and  len(validated_data["DESIG_NM"])>0:          
            design_name = validated_data.get('DESIG_NM')
            convertFrom, convertTo = lang_detect(design_name)
            validated_data["DESIG_NM"], validated_data["DESIG_NM_UR"]  = lang_translate(stringToConvert=design_name, from_lang=convertFrom, to_lang=convertTo)
        
        if "DESIG_DESC" in validated_data  and  len(validated_data["DESIG_DESC"])>0:          
            design_desc = validated_data.get('DESIG_DESC', None)
            convertFrom, convertTo = lang_detect(design_desc)
            validated_data["DESIG_DESC"], validated_data["DESIG_DESC_UR"]  = lang_translate(stringToConvert=design_desc, from_lang=convertFrom, to_lang=convertTo)

        instance.DESIG_NM = validated_data.get('DESIG_NM', instance.DESIG_NM)
        instance.DESIG_NM_UR = validated_data.get('DESIG_NM_UR', instance.DESIG_NM_UR)
        instance.DESIG_DESC = validated_data.get('DESIG_DESC', instance.DESIG_DESC)
        instance.DESIG_DESC_UR = validated_data.get('DESIG_DESC_UR', instance.DESIG_DESC_UR)

        instance.save()
        return instance