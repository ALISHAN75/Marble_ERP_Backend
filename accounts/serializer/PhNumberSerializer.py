from rest_framework import serializers
# models imports
from accounts.model.Account import Phone_Numbers


class PhNumberSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = Phone_Numbers
    fields = "__all__"

  def create(self, validate_data):  
    created = Phone_Numbers.objects.create(**validate_data)
    return created
  

  
  def update(self, instance, validated_data):       
    instance.IS_PRIMARY = validated_data.get('IS_PRIMARY', instance.IS_PRIMARY)
    instance.PH_NUM = validated_data.get('PH_NUM', instance.PH_NUM)
    instance.IS_CELL = validated_data.get('IS_CELL', instance.IS_CELL)
    instance.save()
        
    return instance

  