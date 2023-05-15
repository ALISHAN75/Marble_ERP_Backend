from rest_framework import serializers
# models imports
from hrm.model.Employee_Departments import Employee_Departments
from marble_erp.utils.langDetector import lang_detect
from marble_erp.utils.lang_translate import lang_translate

class DepartmentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee_Departments
        fields = (
            'EMP_DEPT_ID',
            'DEPT_NM',
            'DEPT_NM_UR',
            'DEPT_DESC',
            'DEPT_DESC_UR',
            'IS_ACTIVE',
            'REC_ADD_DT',
            'REC_ADD_BY',
            'REC_MOD_DT',
            'REC_MOD_BY'
        )



    def create(self, validate_data):
        if "DEPT_NM" in validate_data:          
            dep_name = validate_data.get('DEPT_NM')
            convertFrom, convertTo = lang_detect(dep_name)
            validate_data["DEPT_NM"], validate_data["DEPT_NM_UR"]  = lang_translate(stringToConvert=dep_name, from_lang=convertFrom, to_lang=convertTo)
        
        if "DEPT_DESC" in validate_data:          
            dep_desc = validate_data.get('DEPT_DESC', None)
            convertFrom, convertTo = lang_detect(dep_desc)
            validate_data["DEPT_DESC"], validate_data["DEPT_DESC_UR"]  = lang_translate(stringToConvert=dep_desc, from_lang=convertFrom, to_lang=convertTo)

        return Employee_Departments.objects.create(**validate_data)

    def update(self, instance, validated_data):
        if "DEPT_NM" in validated_data:          
            dep_name = validated_data.get('DEPT_NM')
            convertFrom, convertTo = lang_detect(dep_name)
            validated_data["DEPT_NM"], validated_data["DEPT_NM_UR"]  = lang_translate(stringToConvert=dep_name, from_lang=convertFrom, to_lang=convertTo)
        
        if "DEPT_DESC" in validated_data:          
            dep_desc = validated_data.get('DEPT_DESC', None)
            convertFrom, convertTo = lang_detect(dep_desc)
            validated_data["DEPT_DESC"], validated_data["DEPT_DESC_UR"]  = lang_translate(stringToConvert=dep_desc, from_lang=convertFrom, to_lang=convertTo)

        instance.DEPT_NM = validated_data.get('DEPT_NM', instance.DEPT_NM)
        instance.DEPT_NM_UR = validated_data.get('DEPT_NM_UR', instance.DEPT_NM_UR)
        instance.DEPT_DESC = validated_data.get('DEPT_DESC', instance.DEPT_DESC)
        instance.DEPT_DESC_UR = validated_data.get('DEPT_DESC_UR', instance.DEPT_DESC_UR)

        instance.save()
        return instance

