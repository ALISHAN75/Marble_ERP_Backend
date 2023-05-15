from rest_framework import serializers
# models imports
from inventory.model.Quotations import Quotations, Quotations_Items
from inventory.model.Orders import Order_items, Orders
from inventory.serializers.ProductsSerializer import ProductsSerializer
from inventory.serializers.ProductsSerializer import ProductsDetailSerializer
from inventory.serializers.ProductSizesSerializer import ProductSizesSerializer
from inventory.serializers.ProductSizesSerializer import ProductSizesSerializer
# Utils
from marble_erp.utils.langDetector import lang_detect
from marble_erp.utils.lang_translate import lang_translate

class AddGeneralQuotationItemsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Quotations_Items
        fields = "__all__"
        extra_kwargs = {'REQ_QTY': {'required': True} , 
                        'GEN_PROD_NM': {'required': True} ,
                        'PROD_UNIT_COST': {'required': True} ,
                        'PROD_TOTL_PRICE ': {'required': True} ,
                        'REQ_SQFT': {'required': False} ,
                        'PAY_SQFT': {'required': False} ,
                        'PAY_QTY': {'required': False} ,
                        'IS_SECTIONED': {'required': False} ,
                        'IS_GOLA': {'required': False} ,
                        'IS_SIZED': {'required': False} , 
                        'IS_POLISHED': {'required': False} , 
                        }


    def create(self, validate_data):
        if "GEN_PROD_NM" in validate_data and len(validate_data["GEN_PROD_NM"])>0:          
            GEN_PROD_NM = validate_data.get('GEN_PROD_NM')
            convertFrom, convertTo = lang_detect(GEN_PROD_NM)
            validate_data["GEN_PROD_NM"], validate_data["GEN_PROD_NM_UR"]  = lang_translate(stringToConvert=GEN_PROD_NM, from_lang=convertFrom, to_lang=convertTo)
        if "PROD_DESC" in validate_data and len(validate_data["PROD_DESC"])>0:          
                PROD_DESC = validate_data.get('PROD_DESC')
                convertFrom, convertTo = lang_detect(PROD_DESC)
                validate_data["PROD_DESC"], validate_data["PROD_DESC_UR"]  = lang_translate(stringToConvert=PROD_DESC, from_lang=convertFrom, to_lang=convertTo)

        
        created_order = Quotations_Items.objects.create(**validate_data)
        return created_order  


    def update(self, instance, validated_data):
        if "GEN_PROD_NM" in validated_data and len(validated_data["GEN_PROD_NM"])>0:          
                GEN_PROD_NM = validated_data.get('GEN_PROD_NM')
                convertFrom, convertTo = lang_detect(GEN_PROD_NM)
                validated_data["GEN_PROD_NM"], validated_data["GEN_PROD_NM_UR"]  = lang_translate(stringToConvert=GEN_PROD_NM, from_lang=convertFrom, to_lang=convertTo)
        if "PROD_DESC" in validated_data and len(validated_data["PROD_DESC"])>0:          
                PROD_DESC = validated_data.get('PROD_DESC')
                convertFrom, convertTo = lang_detect(PROD_DESC)
                validated_data["PROD_DESC"], validated_data["PROD_DESC_UR"]  = lang_translate(stringToConvert=PROD_DESC, from_lang=convertFrom, to_lang=convertTo)


        instance.IS_GEN_PROD = validated_data.get('IS_GEN_PROD', instance.IS_GEN_PROD)
        instance.GEN_PROD_NM = validated_data.get('GEN_PROD_NM', instance.GEN_PROD_NM)
        instance.GEN_PROD_NM_UR = validated_data.get('GEN_PROD_NM_UR', instance.GEN_PROD_NM_UR)

        instance.REQ_QTY = validated_data.get('REQ_QTY', instance.REQ_QTY)
        instance.REQ_SQFT = validated_data.get('REQ_SQFT', instance.REQ_SQFT)
        instance.PAY_SQFT = validated_data.get('PAY_SQFT', instance.PAY_SQFT)
        instance.PAY_QTY = validated_data.get('PAY_QTY', instance.PAY_QTY)
        instance.PROD_UNIT_COST = validated_data.get('PROD_UNIT_COST', instance.PROD_UNIT_COST)
        instance.PROD_TOTL_PRICE = validated_data.get('PROD_TOTL_PRICE', instance.PROD_TOTL_PRICE)
        instance.PROD_DESC = validated_data.get('PROD_DESC', instance.PROD_DESC)
        instance.PROD_DESC_UR = validated_data.get('PROD_DESC_UR', instance.PROD_DESC_UR)
        instance.IS_SECTIONED = validated_data.get('IS_SECTIONED', instance.IS_SECTIONED)
        instance.IS_GOLA = validated_data.get('IS_GOLA', instance.IS_GOLA)
        instance.IS_SIZED = validated_data.get('IS_SIZED', instance.IS_SIZED)
        instance.IS_POLISHED = validated_data.get('IS_POLISHED', instance.IS_POLISHED)
        instance.IS_DLVRD = validated_data.get('IS_DLVRD', instance.IS_DLVRD)
        instance.DLVRD_QTY = validated_data.get('DLVRD_QTY', instance.DLVRD_QTY)
        instance.REC_ADD_DT = validated_data.get('REC_ADD_DT', instance.REC_ADD_DT)
        instance.REC_ADD_BY = validated_data.get('REC_ADD_BY', instance.REC_ADD_BY)
        instance.REC_MOD_DT = validated_data.get('REC_MOD_DT', instance.REC_MOD_DT)
        instance.REC_MOD_BY = validated_data.get('REC_MOD_BY', instance.REC_MOD_BY)
        instance.PAY_SIZE_ID = validated_data.get('PAY_SIZE_ID', instance.PAY_SIZE_ID)
        instance.PRODUCT_ID = validated_data.get('PRODUCT_ID', instance.PRODUCT_ID)
        instance.DLVRY_SIZE_ID = validated_data.get('DLVRY_SIZE_ID', instance.DLVRY_SIZE_ID)

        instance.save()
        return instance

class AddGeneralOrderItemsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order_items
        fields = "__all__"
        extra_kwargs = {'REQ_QTY': {'required': True} , 
                        'GEN_PROD_NM': {'required': True} ,
                        'PROD_UNIT_COST': {'required': True} ,
                        'PROD_TOTL_PRICE ': {'required': True} ,
                        'REQ_SQFT': {'required': False} ,
                        'PAY_SQFT': {'required': False} ,
                        'PAY_QTY': {'required': False} ,
                        'IS_SECTIONED': {'required': False} ,
                        'IS_GOLA': {'required': False} ,
                        'IS_SIZED': {'required': False} , 
                        'IS_POLISHED': {'required': False} , 
                        }


    def create(self, validate_data):
        if "GEN_PROD_NM" in validate_data and len(validate_data["GEN_PROD_NM"])>0:          
            GEN_PROD_NM = validate_data.get('GEN_PROD_NM')
            convertFrom, convertTo = lang_detect(GEN_PROD_NM)
            validate_data["GEN_PROD_NM"], validate_data["GEN_PROD_NM_UR"]  = lang_translate(stringToConvert=GEN_PROD_NM, from_lang=convertFrom, to_lang=convertTo)
        if "PROD_DESC" in validate_data and len(validate_data["PROD_DESC"])>0:          
                PROD_DESC = validate_data.get('PROD_DESC')
                convertFrom, convertTo = lang_detect(PROD_DESC)
                validate_data["PROD_DESC"], validate_data["PROD_DESC_UR"]  = lang_translate(stringToConvert=PROD_DESC, from_lang=convertFrom, to_lang=convertTo)

        created_order = Order_items.objects.create(**validate_data)
        return created_order  
            
    def update(self, instance, validated_data):
        if "GEN_PROD_NM" in validated_data and len(validated_data["GEN_PROD_NM"])>0:          
                GEN_PROD_NM = validated_data.get('GEN_PROD_NM')
                convertFrom, convertTo = lang_detect(GEN_PROD_NM)
                validated_data["GEN_PROD_NM"], validated_data["GEN_PROD_NM_UR"]  = lang_translate(stringToConvert=GEN_PROD_NM, from_lang=convertFrom, to_lang=convertTo)
        if "PROD_DESC" in validated_data and len(validated_data["PROD_DESC"])>0:          
                PROD_DESC = validated_data.get('PROD_DESC')
                convertFrom, convertTo = lang_detect(PROD_DESC)
                validated_data["PROD_DESC"], validated_data["PROD_DESC_UR"]  = lang_translate(stringToConvert=PROD_DESC, from_lang=convertFrom, to_lang=convertTo)


        instance.IS_GEN_PROD = validated_data.get('IS_GEN_PROD', instance.IS_GEN_PROD)
        instance.GEN_PROD_NM = validated_data.get('GEN_PROD_NM', instance.GEN_PROD_NM)
        instance.GEN_PROD_NM_UR = validated_data.get('GEN_PROD_NM_UR', instance.GEN_PROD_NM_UR)

        instance.REQ_QTY = validated_data.get('REQ_QTY', instance.REQ_QTY)
        instance.REQ_SQFT = validated_data.get('REQ_SQFT', instance.REQ_SQFT)
        instance.PAY_SQFT = validated_data.get('PAY_SQFT', instance.PAY_SQFT)
        instance.PAY_QTY = validated_data.get('PAY_QTY', instance.PAY_QTY)
        instance.PROD_UNIT_COST = validated_data.get('PROD_UNIT_COST', instance.PROD_UNIT_COST)
        instance.PROD_TOTL_PRICE = validated_data.get('PROD_TOTL_PRICE', instance.PROD_TOTL_PRICE)
        instance.PROD_DESC = validated_data.get('PROD_DESC', instance.PROD_DESC)
        instance.PROD_DESC_UR = validated_data.get('PROD_DESC_UR', instance.PROD_DESC_UR)
        instance.IS_SECTIONED = validated_data.get('IS_SECTIONED', instance.IS_SECTIONED)
        instance.IS_GOLA = validated_data.get('IS_GOLA', instance.IS_GOLA)
        instance.IS_SIZED = validated_data.get('IS_SIZED', instance.IS_SIZED)
        instance.IS_POLISHED = validated_data.get('IS_POLISHED', instance.IS_POLISHED)
        instance.IS_DLVRD = validated_data.get('IS_DLVRD', instance.IS_DLVRD)
        instance.DLVRD_QTY = validated_data.get('DLVRD_QTY', instance.DLVRD_QTY)
        instance.REC_ADD_DT = validated_data.get('REC_ADD_DT', instance.REC_ADD_DT)
        instance.REC_ADD_BY = validated_data.get('REC_ADD_BY', instance.REC_ADD_BY)
        instance.REC_MOD_DT = validated_data.get('REC_MOD_DT', instance.REC_MOD_DT)
        instance.REC_MOD_BY = validated_data.get('REC_MOD_BY', instance.REC_MOD_BY)
        instance.PAY_SIZE_ID = validated_data.get('PAY_SIZE_ID', instance.PAY_SIZE_ID)
        instance.PRODUCT_ID = validated_data.get('PRODUCT_ID', instance.PRODUCT_ID)
        instance.DLVRY_SIZE_ID = validated_data.get('DLVRY_SIZE_ID', instance.DLVRY_SIZE_ID)

        instance.save()
        return instance



class OrderItemsSerializer(serializers.ModelSerializer):

    PRODUCT_ID = ProductsDetailSerializer()
    PAY_SIZE_ID = ProductSizesSerializer()
    DLVRY_SIZE_ID = ProductSizesSerializer()

    class Meta:
        model = Order_items
        fields = "__all__"

        
class OrderItemsSerializer(serializers.ModelSerializer):

    PRODUCT_ID = ProductsDetailSerializer()
    PAY_SIZE_ID = ProductSizesSerializer()
    DLVRY_SIZE_ID = ProductSizesSerializer()

    class Meta:
        model = Order_items
        fields = "__all__"
    


class AddOrderItemsSerializer(serializers.ModelSerializer):

    PROD_CAT = serializers.CharField(max_length=45)
    PROD_NAME = serializers.CharField(max_length=45)
    PROD_USAGE = serializers.CharField(max_length=45)
    PAY_THICKNESS = serializers.DecimalField(max_digits=10, decimal_places=2)
    PAY_LENGTH = serializers.DecimalField(max_digits=10, decimal_places=2)
    PAY_WIDTH = serializers.DecimalField(max_digits=10, decimal_places=2)
    REQ_THICKNESS = serializers.DecimalField(max_digits=10, decimal_places=2)
    REQ_LENGTH = serializers.DecimalField(max_digits=10, decimal_places=2)
    REQ_WIDTH = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Order_items
        fields = "__all__"


        


    def create(self, validate_data):
        PROD_CAT = validate_data.pop('PROD_CAT')
        PROD_NAME = validate_data.pop('PROD_NAME')
        PROD_USAGE = validate_data.pop('PROD_USAGE')
        PAY_THICKNESS = validate_data.pop('PAY_THICKNESS')
        PAY_LENGTH = validate_data.pop('PAY_LENGTH')
        PAY_WIDTH = validate_data.pop('PAY_WIDTH')
        REQ_THICKNESS = validate_data.pop('REQ_THICKNESS')
        REQ_LENGTH = validate_data.pop('REQ_LENGTH')
        REQ_WIDTH = validate_data.pop('REQ_WIDTH')

        if "GEN_PROD_NM" in validate_data and len(validate_data["GEN_PROD_NM"])>0:          
            GEN_PROD_NM = validate_data.get('GEN_PROD_NM')
            convertFrom, convertTo = lang_detect(GEN_PROD_NM)
            validate_data["GEN_PROD_NM"], validate_data["GEN_PROD_NM_UR"]  = lang_translate(stringToConvert=GEN_PROD_NM, from_lang=convertFrom, to_lang=convertTo)

        created_order = Order_items.objects.create(**validate_data)
        return created_order


    def update(self, instance, validated_data):
        if "GEN_PROD_NM" in validated_data and len(validated_data["GEN_PROD_NM"])>0:          
                GEN_PROD_NM = validated_data.get('GEN_PROD_NM')
                convertFrom, convertTo = lang_detect(GEN_PROD_NM)
                validated_data["GEN_PROD_NM"], validated_data["GEN_PROD_NM_UR"]  = lang_translate(stringToConvert=GEN_PROD_NM, from_lang=convertFrom, to_lang=convertTo)


        instance.IS_GEN_PROD = validated_data.get('IS_GEN_PROD', instance.IS_GEN_PROD)
        instance.GEN_PROD_NM = validated_data.get('GEN_PROD_NM', instance.GEN_PROD_NM)
        instance.GEN_PROD_NM_UR = validated_data.get('GEN_PROD_NM_UR', instance.GEN_PROD_NM_UR)

        instance.REQ_QTY = validated_data.get('REQ_QTY', instance.REQ_QTY)
        instance.REQ_SQFT = validated_data.get('REQ_SQFT', instance.REQ_SQFT)
        instance.PAY_SQFT = validated_data.get('PAY_SQFT', instance.PAY_SQFT)
        instance.PAY_QTY = validated_data.get('PAY_QTY', instance.PAY_QTY)
        instance.PROD_UNIT_COST = validated_data.get('PROD_UNIT_COST', instance.PROD_UNIT_COST)
        instance.PROD_TOTL_PRICE = validated_data.get('PROD_TOTL_PRICE', instance.PROD_TOTL_PRICE)
        instance.PROD_DESC = validated_data.get('PROD_DESC', instance.PROD_DESC)
        instance.PROD_DESC_UR = validated_data.get('PROD_DESC_UR', instance.PROD_DESC_UR)
        instance.IS_SECTIONED = validated_data.get('IS_SECTIONED', instance.IS_SECTIONED)
        instance.IS_GOLA = validated_data.get('IS_GOLA', instance.IS_GOLA)
        instance.IS_SIZED = validated_data.get('IS_SIZED', instance.IS_SIZED)
        instance.IS_POLISHED = validated_data.get('IS_POLISHED', instance.IS_POLISHED)
        instance.IS_DLVRD = validated_data.get('IS_DLVRD', instance.IS_DLVRD)
        instance.DLVRD_QTY = validated_data.get('DLVRD_QTY', instance.DLVRD_QTY)
        instance.REC_ADD_DT = validated_data.get('REC_ADD_DT', instance.REC_ADD_DT)
        instance.REC_ADD_BY = validated_data.get('REC_ADD_BY', instance.REC_ADD_BY)
        instance.REC_MOD_DT = validated_data.get('REC_MOD_DT', instance.REC_MOD_DT)
        instance.REC_MOD_BY = validated_data.get('REC_MOD_BY', instance.REC_MOD_BY)
        instance.PAY_SIZE_ID = validated_data.get('PAY_SIZE_ID', instance.PAY_SIZE_ID)
        instance.PRODUCT_ID = validated_data.get('PRODUCT_ID', instance.PRODUCT_ID)
        instance.DLVRY_SIZE_ID = validated_data.get('DLVRY_SIZE_ID', instance.DLVRY_SIZE_ID)

        instance.save()
        return instance

        