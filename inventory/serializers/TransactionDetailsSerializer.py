from rest_framework import serializers
from inventory.model.Inventory import Transaction_Details


class TransactionDetailsSerializer(serializers.ModelSerializer):

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
            'IS_AVLBL',
            'AVLBL_QTY',
            'AVLBL_SQFT',
            'INV_TRANS_ID',
            'PROD_ID',
            'SIZE_ID',
            'REC_ADD_DT',
            'REC_ADD_BY',
        )
        depth = 2


class AddTransactionDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction_Details
        fields = "__all__"

        
       

# create and update



class AddInvAdjustmentSerializer(serializers.ModelSerializer):

    CAT_ID = serializers.IntegerField()
    USAGE_ID = serializers.IntegerField()
    NAME_ID = serializers.IntegerField()
    WIDTH = serializers.DecimalField(max_digits=10, decimal_places=2)
    LENGTH = serializers.DecimalField(max_digits=10, decimal_places=2)
    THICKNESS = serializers.DecimalField(max_digits=10, decimal_places=2)
    TOTAL_PROD_UNIT_COST = serializers.DecimalField(max_digits=10, decimal_places=2)

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
# create and update