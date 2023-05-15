from rest_framework import serializers
# models imports
from inventory.model.Inventory import Inventory_Transactions, Transaction_Details
from inventory.serializers.InventorySerializer import Final_Details
# Utils
from marble_erp.utils.langDetector import lang_detect
from marble_erp.utils.lang_translate import lang_translate

class InvRecoverySerializer(serializers.ModelSerializer):

    INV_DETAILS = Final_Details()

    class Meta:
        model = Inventory_Transactions
        fields = "__all__"
       
# create and update
    def create(self, validate_data):
        inv_detail_final = validate_data.pop('INV_DETAILS')

        if "TRANS_TYP" in validate_data:          
            TRANS_TYP = validate_data.pop('TRANS_TYP')
            convertFrom, convertTo = lang_detect(TRANS_TYP)
            validate_data["TRANS_TYP"], validate_data["TRANS_TYP_UR"]  = lang_translate(stringToConvert=TRANS_TYP, from_lang=convertFrom, to_lang=convertTo)
       
        created_inventory = Inventory_Transactions.objects.create(**validate_data)
        return created_inventory

    def update(self, instance, validated_data):
        inv_detail_final = validated_data.pop('INV_DETAILS')

        if "TRANS_TYP" in validated_data:          
            TRANS_TYP = validated_data.pop('TRANS_TYP')
            convertFrom, convertTo = lang_detect(TRANS_TYP)
            validated_data["TRANS_TYP"], validated_data["TRANS_TYP_UR"]  = lang_translate(stringToConvert=TRANS_TYP, from_lang=convertFrom, to_lang=convertTo)
        
        instance.TRANS_TYP = validated_data.get('TRANS_TYP', instance.TRANS_TYP)
        instance.TRANS_TYP_UR = validated_data.get('TRANS_TYP_UR', instance.TRANS_TYP_UR)

        instance.save()
        return instance


class InvDetailsRecoverySerializer(serializers.ModelSerializer):

    CAT_ID = serializers.IntegerField()
    USAGE_ID = serializers.IntegerField()
    NAME_ID = serializers.IntegerField()
    WIDTH = serializers.DecimalField(max_digits=10, decimal_places=2)
    LENGTH = serializers.DecimalField(max_digits=10, decimal_places=2)
    THICKNESS = serializers.DecimalField(max_digits=10, decimal_places=2)
    TOTAL_PROD_UNIT_COST = serializers.DecimalField(
        max_digits=10, decimal_places=2)

    class Meta:
        model = Transaction_Details
        fields = (
            'INV_TRANS_DETAIL_ID',
            'IS_LAST_REC',
            'QTY',
            'QTY_SQFT',
            'TOTAL_PROD_UNIT_COST',
            'TOTAL_AVG_PROD_UNIT_COST',
            'IS_SECTIONED',
            'IS_GOLA',
            'IS_SIZED',
            'IS_POLISHED',
            'INV_TRANS_ID',
            'CAT_ID',
            'USAGE_ID',
            'NAME_ID',
            'WIDTH',
            'LENGTH',
            'THICKNESS',
            'REC_ADD_DT',
            'REC_ADD_BY',
        )
