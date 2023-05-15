from rest_framework import serializers
from django.contrib.auth.models import Group
# serializers
from accounts.serializer.PermissionsSerialzer import PermissionRegisterSerializer
# Utils
from marble_erp.utils.langDetector import lang_detect
from marble_erp.utils.lang_translate import lang_translate


class GroupSerializer(serializers.ModelSerializer):
  # permissions = serializers.ListField(child = serializers.IntegerField())
  user_permissions = PermissionRegisterSerializer(many=True)

  class Meta:
    model = Group
    fields = [
      'name',
      'user_permissions'
    ]

  def create(self, validate_data):
    if "name" in validate_data:          
            name = validate_data["name"]
            convertFrom, convertTo = lang_detect(name)
            validate_data["name"], validate_data["name_UR"]  = lang_translate(stringToConvert=name, from_lang=convertFrom, to_lang=convertTo)
    new_grp = Group.objects.create(**validate_data)


    return new_grp

  
class GroupListSerializer(serializers.ModelSerializer):

  class Meta:
    model = Group
    fields = (
        'id',
        'name'
        )

  def create(self, validate_data):
    if "name" in validate_data:          
            name = validate_data["name"]
            convertFrom, convertTo = lang_detect(name)
            validate_data["name"], validate_data["name_UR"]  = lang_translate(stringToConvert=name, from_lang=convertFrom, to_lang=convertTo)
    new_grp = Group.objects.create(**validate_data)


    return new_grp

  def update(self, instance, validated_data):
    if "name" in validated_data:          
            name = validated_data["name"]
            convertFrom, convertTo = lang_detect(name)
            validated_data["name"], validated_data["name_UR"]  = lang_translate(stringToConvert=name, from_lang=convertFrom, to_lang=convertTo)
    instance.name = validated_data.get('name', instance.name)
    instance.name_UR = validated_data.get('name_UR', instance.name_UR)
    instance.save()


    return instance
