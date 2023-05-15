from rest_framework import serializers
from inventory.serializers.OrderItemsSerializer import OrderItemsSerializer
# models imports
from logistics.model.Deliveries import Delivery_Items


class AddDeliveryItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Delivery_Items
        fields = '__all__'
# create and update

class DeliveryItemsSerializer(serializers.ModelSerializer):
    ORDR_ITEM_ID = OrderItemsSerializer(read_only=True)

    class Meta:
        model = Delivery_Items
        fields = '__all__'
        # depth = 1
