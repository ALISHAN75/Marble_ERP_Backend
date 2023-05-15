from rest_framework import serializers
from inventory.model.Breakage import Breakage

class AddBreakageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Breakage
        fields =  (
            'AVLBL_SQFT',
        )
        # fields = "__all__"

class BreakageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Breakage
        fields = "__all__"


