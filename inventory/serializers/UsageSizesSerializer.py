from rest_framework import serializers
# models imports
from inventory.model.ProductUsageSizes import ProductUsageSizes


class UsageSizesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductUsageSizes
        fields = '__all__'
  
        depth: 2
