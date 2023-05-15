from rest_framework import serializers
# models imports
from inventory.model.Products import Products


class ProductsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Products
        fields = (
            'PRODUCT_ID',
            'PROD_NM_ID',
            'CAT_ID',
            'USAGE_ID',
            'PROD_AVLBL_QTY',
            'IS_ACTIVE',
            'REC_ADD_DT',
            'REC_ADD_BY',
            'REC_MOD_DT',
            'REC_MOD_BY'
        )



class ProductsDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Products
        fields = (
            'PRODUCT_ID',
            'PROD_NM_ID',
            'CAT_ID',
            'USAGE_ID',
            'PROD_AVLBL_QTY',
            'IS_ACTIVE',
            'REC_ADD_DT',
            'REC_ADD_BY',
            'REC_MOD_DT',
            'REC_MOD_BY'
        )
        depth = 1


class AddProductsSerializer(serializers.ModelSerializer):

    # PROD_NM_ID = serializers.CharField()
    # CAT_ID = serializers.CharField()
    # USAGE_ID = serializers.CharField()

    class Meta:
        model = Products
        fields = (
            'PRODUCT_ID',
            'PROD_NM_ID',
            'CAT_ID',
            'USAGE_ID',
            'PROD_AVLBL_QTY',
            'IS_ACTIVE',
            'REC_ADD_DT',
            'REC_ADD_BY',
            'REC_MOD_DT',
            'REC_MOD_BY'
        )
        # depth=1

        # def validate(self, attrs):

        #   initial_inv = attrs.get('I_DETAILS')
        #   final_inv_list = attrs.get('F_DETAILS')
        #   transaction_type = attrs.get('TRANS_TYP')
        #   labour_qty_sqft = attrs.get('LABOUR_SQFT')

        #   return attrs

        # def create(self, validate_data):
        #   inv_detail_initial = validate_data.pop('I_DETAILS')
        #   inv_detail_final = validate_data.pop('F_DETAILS')

        #   created_inventory = Inventory_Transactions.objects.create(**validate_data)

        #   # get request user
        #   request = self.context.get("request")
        #   # for inv_detail in  inv_detail_final:
        #   #   inv_detail["INV_TRANS_ID"] = created_inventory
        #   #   if request and hasattr(request, "user"):
        #   #     inv_detail["REC_ADD_BY"] = request.user.id
        #   #     inv_detail["REC_MOD_BY"] = request.user.id
        #   #   Transaction_Details.objects.create(**inv_detail)

        #   # for role in roles:
        #   #  role = Group.objects.get(id=role)
        #   #  created_user.groups.add(role)

        #   return created_inventory
