from rest_framework import serializers
# models imports
from inventory.model.Orders import Orders , Order_items
from accounts.serializer.UsersSerializer import AccountsSerializer
from hrm.serializer.EmployeeSerializer import EmployeeSerializer
from finance.serializer.CurrencySerializer import CurrencySerializer
from inventory.serializers.OrderItemsSerializer import OrderItemsSerializer, AddOrderItemsSerializer , AddGeneralOrderItemsSerializer
# Utils
from marble_erp.utils.langDetector import lang_detect
from marble_erp.utils.lang_translate import lang_translate

class OrderSerializer(serializers.ModelSerializer):
    ORDER_ITEMS = OrderItemsSerializer(many=True)

    class Meta:
        model = Orders
        fields = "__all__"
        depth = 2



class AddOrderSerializer(serializers.ModelSerializer):
    # ORDER_ITEMS = AddOrderItemsSerializer(many=True)
    # ORDER_ITEMS = AddGeneralOrderItemsSerializer(many=True)

    class Meta:
        model = Orders
        fields = "__all__"

       
    def validate(self, attrs):
      IS_SALE = attrs.get('IS_SALE')
      MRCHNT_ACCT_ID = attrs.get('MRCHNT_ACCT_ID' , None)
      CUST_ACCT_ID = attrs.get('CUST_ACCT_ID' , None)
      if (IS_SALE == 1 and not CUST_ACCT_ID):
        raise serializers.ValidationError({"error" :  "Customer Account is required"  , "error_ur" : "کسٹمر اکاؤنٹ درکار ہے۔" } )
      if (IS_SALE == 0 and not MRCHNT_ACCT_ID) :
        raise serializers.ValidationError( {"error" :  "Merchant Account is required" , "error_ur" : "مرچنٹ اکاؤنٹ درکار ہے۔" } )
      return attrs

    def create(self, validate_data):
        if "ORDER_ITEMS" in validate_data:
            ORDER_ITEMS = validate_data.pop('ORDER_ITEMS')
        if "ORDER_DETAIL" in validate_data:
            ORDER_DETAIL = validate_data.pop('ORDER_DETAIL')
            convertFrom, convertTo = lang_detect(ORDER_DETAIL)
            validate_data["ORDER_DETAIL"], validate_data["ORDER_DETAIL_UR"]  = lang_translate(stringToConvert=ORDER_DETAIL, from_lang=convertFrom, to_lang=convertTo)
        created_order = Orders.objects.create(**validate_data)
        return created_order

    def update(self, instance, validated_data):
        if "ORDER_ITEMS" in validated_data:
            ORDER_ITEMS = validated_data.pop('ORDER_ITEMS')
        

        if "ORDER_DETAIL" in validated_data:
            ORDER_DETAIL = validated_data.pop('ORDER_DETAIL')
            convertFrom, convertTo = lang_detect(ORDER_DETAIL)
            validated_data["ORDER_DETAIL"], validated_data["ORDER_DETAIL_UR"]  = lang_translate(stringToConvert=ORDER_DETAIL, from_lang=convertFrom, to_lang=convertTo)
            # validated_data["ORDR_NO"], validated_data["ORDR_NO_UR"]  = lang_translate(stringToConvert=instance.ORDR_NO, from_lang=convertFrom, to_lang=convertTo)
     
        instance.IS_SALE = validated_data.get('IS_SALE', instance.IS_SALE)
        instance.ORDR_DT = validated_data.get('ORDR_DT', instance.ORDR_DT)
        instance.ORDR_TOTAL_wTAX = validated_data.get('ORDR_TOTAL_wTAX', instance.ORDR_TOTAL_wTAX)
        instance.TAX_PRCNT = validated_data.get('TAX_PRCNT', instance.TAX_PRCNT)
        instance.ORDR_TOTAL_no_TAX = validated_data.get('ORDR_TOTAL_no_TAX', instance.ORDR_TOTAL_no_TAX)
        instance.ORDER_DETAIL = validated_data.get('ORDER_DETAIL', instance.ORDER_DETAIL)
        instance.ORDER_DETAIL_UR = validated_data.get('ORDER_DETAIL_UR', instance.ORDER_DETAIL_UR)
        instance.IS_ACTIVE = validated_data.get('IS_ACTIVE', instance.IS_ACTIVE)
        instance.CUST_ACCT_ID = validated_data.get('CUST_ACCT_ID', instance.CUST_ACCT_ID)
        instance.MRCHNT_ACCT_ID = validated_data.get('MRCHNT_ACCT_ID', instance.MRCHNT_ACCT_ID)
        instance.ORDR_BY_EMP_ID = validated_data.get('ORDR_BY_EMP_ID', instance.ORDR_BY_EMP_ID)
        instance.DELVRY_STS = validated_data.get('DELVRY_STS', instance.DELVRY_STS)
        instance.ADV_PAYMENT = validated_data.get('ADV_PAYMENT', instance.ADV_PAYMENT)
        instance.REC_ADD_BY = validated_data.get('REC_ADD_BY', instance.REC_ADD_BY)
        instance.REC_MOD_BY = validated_data.get('REC_MOD_BY', instance.REC_MOD_BY)

        instance.save()
        return instance


# others
class MerchantOrderSerializer(serializers.ModelSerializer):

    MRCHNT = AccountsSerializer(read_only=True)
    # ORDR_BY_EMP = EmployeeSerializer(read_only=True)
    ORDER_ITEMS = OrderItemsSerializer(read_only=True, many=True)

    class Meta:
        model = Orders
        fields = (
            'ORDR_ID',
            'IS_SALE',
            'IS_ACTIVE',
            'ORDR_DT',
            # 'ORDR_BY_EMP_ID',
            # 'ORDR_BY_EMP',
            'MRCHNT_ACCT_ID',
            'MRCHNT',
            'ORDER_ITEMS'
        )


class CustomerOrderSerializer(serializers.ModelSerializer):

    CUST = AccountsSerializer(read_only=True)
    # ORDR_BY_EMP = EmployeeSerializer(read_only=True)
    ORDER_ITEMS = OrderItemsSerializer(read_only=True, many=True)

    class Meta:
        model = Orders
        fields = (
            'ORDR_ID',
            'ORDR_DT',
            'IS_SALE',
            'IS_ACTIVE',
            # 'ORDR_BY_EMP_ID',
            # 'ORDR_BY_EMP',
            'CUST_ACCT_ID',
            'CUST',
            'ORDER_ITEMS'
        )
