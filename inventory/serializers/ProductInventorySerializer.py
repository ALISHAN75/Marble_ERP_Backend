from rest_framework import serializers
from inventory.model.Inventory import Transaction_Details


class ProductInventorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction_Details
        fields = (
            'INV_PROD_ID',
            'PROD_ID',
            'SIZE_ID',
            'IS_SECTIONED',
            'IS_GOLA',
            'IS_SIZED',
            'IS_POLISHED',
            'QTY',
            'QTY_SQFT',
            'AVLBL_QTY',
            'AVLBL_SQFT',
            'TOTAL_PROD_UNIT_COST',
            'TOTAL_AVG_PROD_UNIT_COST',
            'IS_AVLBL',
            'REC_ADD_DT',
            'REC_ADD_BY',
            'REC_MOD_DT',
            'REC_MOD_BY'
        )
