from rest_framework import serializers
# models imports
from inventory.model.Quotations import Quotations, Quotations_Items
from accounts.serializer.UsersSerializer import AccountsSerializer
from hrm.serializer.EmployeeSerializer import EmployeeSerializer
from finance.serializer.CurrencySerializer import CurrencySerializer
from inventory.serializers.QuotationsItemsSerializer import AddQuotationsItemsSerializer  , QuotationsItemsSerializer

# Utils
from marble_erp.utils.langDetector import lang_detect
from marble_erp.utils.lang_translate import lang_translate

class QuotationsrSerializer(serializers.ModelSerializer):
    ORDER_ITEMS = QuotationsItemsSerializer(many=True)

    class Meta:
        model = Quotations
        fields = "__all__"
       
        depth = 2

class AddQuotationsSerializer(serializers.ModelSerializer):
    # ORDER_ITEMS = AddQuotationsItemsSerializer(many=True)

    class Meta:
        model = Quotations
        fields = "__all__"


    def create(self, validate_data):
        if "ORDER_ITEMS" in validate_data:
            ORDER_ITEMS = validate_data.pop('ORDER_ITEMS')
        if "ORDER_DETAIL" in validate_data and len(validate_data["ORDER_DETAIL"])>0:
            ORDER_DETAIL = validate_data.pop('ORDER_DETAIL')
            convertFrom, convertTo = lang_detect(ORDER_DETAIL)
            validate_data["ORDER_DETAIL"], validate_data["ORDER_DETAIL_UR"]  = lang_translate(stringToConvert=ORDER_DETAIL, from_lang=convertFrom, to_lang=convertTo)
        if "CUST_NM" in validate_data and len(validate_data["CUST_NM"])>0:
            CUST_NM = validate_data.pop('CUST_NM')
            convertFrom, convertTo = lang_detect(CUST_NM)
            validate_data["CUST_NM"], validate_data["CUST_NM_UR"]  = lang_translate(stringToConvert=CUST_NM, from_lang=convertFrom, to_lang=convertTo)
        created_order = Quotations.objects.create(**validate_data)
        return created_order



    def update(self, instance, validated_data):
        if "ORDER_ITEMS" in validated_data:
            ORDER_ITEMS = validated_data.pop('ORDER_ITEMS')
        if "ORDER_DETAIL" in validated_data and len(validated_data["ORDER_DETAIL"])>0:
            ORDER_DETAIL = validated_data.pop('ORDER_DETAIL')
            convertFrom, convertTo = lang_detect(ORDER_DETAIL)
            validated_data["ORDER_DETAIL"], validated_data["ORDER_DETAIL_UR"]  = lang_translate(stringToConvert=ORDER_DETAIL, from_lang=convertFrom, to_lang=convertTo)     
        if "CUST_NM" in validated_data and len(validated_data["CUST_NM"])>0:
            CUST_NM = validated_data.pop('CUST_NM')
            convertFrom, convertTo = lang_detect(CUST_NM)
            validated_data["CUST_NM"], validated_data["CUST_NM_UR"]  = lang_translate(stringToConvert=CUST_NM, from_lang=convertFrom, to_lang=convertTo)

        
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
        instance.REC_ADD_BY = validated_data.get('REC_ADD_BY', instance.REC_ADD_BY)
        instance.REC_MOD_BY = validated_data.get('REC_MOD_BY', instance.REC_MOD_BY)
        instance.REC_ADD_DT = validated_data.get('REC_ADD_DT', instance.REC_ADD_DT)
        instance.REC_MOD_DT = validated_data.get('REC_MOD_DT', instance.REC_MOD_DT)
        instance.ADV_PAYMENT = validated_data.get('ADV_PAYMENT', instance.ADV_PAYMENT)
        instance.EXPIRY_DT = validated_data.get('EXPIRY_DT', instance.EXPIRY_DT)
        instance.IS_NOW_ORDER = validated_data.get('IS_NOW_ORDER', instance.IS_NOW_ORDER)
        instance.CUST_NM = validated_data.get('CUST_NM', instance.CUST_NM)
        instance.CUST_NM_UR = validated_data.get('CUST_NM_UR', instance.CUST_NM_UR)
        instance.CUST_PHONE = validated_data.get('CUST_PHONE', instance.CUST_PHONE)


        instance.save()
        return instance
