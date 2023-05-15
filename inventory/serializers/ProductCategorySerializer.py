from rest_framework import serializers
# models imports
from inventory.model.ProductCategory import ProductCategory


class ProductCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCategory
        fields = '__all__'
      
