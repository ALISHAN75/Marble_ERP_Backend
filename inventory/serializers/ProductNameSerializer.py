from rest_framework import serializers
# models imports
from inventory.model.ProductName import ProductName


class ProductNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductName
        fields = '__all__'
