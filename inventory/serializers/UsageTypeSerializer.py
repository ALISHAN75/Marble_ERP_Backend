from rest_framework import serializers
# models imports
from inventory.model.UsageType import UsageType


class UsageTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = UsageType
        fields = '__all__'
        
