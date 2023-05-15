from rest_framework import serializers
# models imports
from inventory.model.ProductSizes import ProductSizes


class ProductSizesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductSizes
        fields = '__all__'
