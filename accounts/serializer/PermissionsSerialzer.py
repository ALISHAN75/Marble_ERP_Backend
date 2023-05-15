from rest_framework import serializers
from django.contrib.auth.models import Permission
# Utils
from marble_erp.utils.langDetector import lang_detect
from marble_erp.utils.lang_translate import lang_translate

class PermissionSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = Permission
    fields = '__all__' 
  
  def create(self, validate_data):
    if "name" in validate_data:          
            name = validate_data["name"]
            convertFrom, convertTo = lang_detect(name)
            validate_data["name"], validate_data["name_UR"]  = lang_translate(stringToConvert=name, from_lang=convertFrom, to_lang=convertTo)
    new_grp = Permission.objects.create(**validate_data)


    return new_grp

  def update(self, instance, validated_data):
    if "name" in validated_data:          
            name = validated_data["name"]
            convertFrom, convertTo = lang_detect(name)
            validated_data["name"], validated_data["name_UR"]  = lang_translate(stringToConvert=name, from_lang=convertFrom, to_lang=convertTo)
    instance.name = validated_data.get('name', instance.name)
    instance.name_UR = validated_data.get('name_UR', instance.name_UR)
    instance.content_type_id = validated_data.get('content_type_id', instance.content_type_id)
    instance.codename = validated_data.get('codename', instance.codename)
    instance.save()


class PermissionRegisterSerializer(serializers.ModelSerializer):
  id = serializers.IntegerField()
  status = serializers.BooleanField()

  class Meta:
    model = Permission
    fields = (
      'id',
      'status'
    ) 
    