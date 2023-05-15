from decimal import Decimal
from rest_framework import serializers
# models imports
from inventory.model.Inventory import Inventory_Transactions, Transaction_Details
from inventory.model.ProductInventory import ProductInventory
from inventory.model.ProductSizes import ProductSizes
from inventory.model.Products import Products
# serializers
from inventory.serializers.TransactionDetailsSerializer import AddTransactionDetailsSerializer, TransactionDetailsSerializer
from inventory.serializers.BreakageSerializer import AddBreakageSerializer
# Utils
from marble_erp.utils.langDetector import lang_detect
from marble_erp.utils.lang_translate import lang_translate

class DetailedInventorySerializer(serializers.ModelSerializer):

    TRANSC_DETALS = TransactionDetailsSerializer(read_only=True, many=True)

    class Meta:
        model = Inventory_Transactions
        fields = "__all__"

        depth = 1


class Initial_Details(serializers.Serializer):

    QTY = serializers.DecimalField(max_digits=10, decimal_places=2)
    QTY_SQFT = serializers.DecimalField(max_digits=10, decimal_places=2)
    IS_SECTIONED = serializers.IntegerField()
    IS_GOLA = serializers.IntegerField()
    IS_SIZED = serializers.IntegerField()
    IS_POLISHED = serializers.IntegerField()
    # PROD_ID = serializers.IntegerField()
    NAME_ID = serializers.IntegerField()
    CAT_ID = serializers.IntegerField()
    USAGE_ID = serializers.IntegerField()
    SIZE_ID = serializers.IntegerField()

    class Meta:
        fields = '__all__'


class Final_Details(serializers.Serializer):

    QTY = serializers.DecimalField(max_digits=10, decimal_places=2)
    QTY_SQFT = serializers.DecimalField(max_digits=10, decimal_places=2)
    IS_SECTIONED = serializers.IntegerField()
    IS_GOLA = serializers.IntegerField()
    IS_SIZED = serializers.IntegerField()
    IS_POLISHED = serializers.IntegerField()
    CAT_ID = serializers.IntegerField()
    USAGE_ID = serializers.IntegerField()
    NAME_ID = serializers.IntegerField()
    WIDTH = serializers.DecimalField(max_digits=10, decimal_places=2)
    LENGTH = serializers.DecimalField(max_digits=10, decimal_places=2)
    THICKNESS = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        fields = '__all__'


class AddInvTransactionSerializer(serializers.ModelSerializer):

    I_DETAILS = Initial_Details()
    F_DETAILS = Final_Details(many=True)
    BREAKAGE = AddBreakageSerializer()

    class Meta:
        model = Inventory_Transactions
        fields = "__all__"
        
# create and update
    def getProductSizeById(self, id):
        return ProductSizes.objects.get(SIZE_ID=id)

    def calcSqft(self, length, width, qty):
        return Decimal(round(abs(((width * length) / 144) * qty), 2))

    def checkInitialProduct(self, typeOfTransac, initialProduct):
        try:
            product = Products.objects.get(
                PROD_NM_ID=initialProduct["NAME_ID"], CAT_ID=initialProduct["CAT_ID"], USAGE_ID=initialProduct["USAGE_ID"])
        except Products.DoesNotExist:
            raise serializers.ValidationError({"error" : "Product does not exist" ,  "error_ur" : "پروڈکٹ موجود نہیں ہے۔" })
        
        if typeOfTransac == "Purchase": return
        try:
            product = ProductInventory.objects.get(
                PROD_ID=product.PRODUCT_ID,
                SIZE_ID=initialProduct["SIZE_ID"],
                IS_SIZED=initialProduct["IS_SIZED"],
                IS_SECTIONED=initialProduct["IS_SECTIONED"],
                IS_POLISHED=initialProduct["IS_POLISHED"],
                IS_GOLA=initialProduct["IS_GOLA"]
                )
            if Decimal(round(abs(initialProduct["QTY"]), 2)) > product.AVLBL_QTY:
                raise serializers.ValidationError({"error" : "Quantity must be less than or equal to stock" ,  "error_ur" : "مقدار اسٹاک سے کم یا اس کے برابر ہونی چاہیے"})
        except ProductInventory.DoesNotExist:
            raise serializers.ValidationError({"error" : "Product does not exist in Inventory" ,  "error_ur" : "پروڈکٹ انوینٹری میں موجود نہیں ہے" })

    def initialSqftCheck(self, length, width, qty, sqft):
        if Decimal(round(abs(sqft), 2)) != self.calcSqft(length, width, qty):
            raise serializers.ValidationError({"error" : "Initial Inventory Item QTY_SQFT must be equal to  (LENGTH x WIDTH / 144) x QTY" , "error_ur" : "(LENGTH x WIDTH / 144) x QTY کے برابر ہونا چاہیے  QTY_SQFT ابتدائی انوینٹری آئٹم" })

    def finalSqftCheck(self, length, width, qty, sqft):
        if Decimal(round(abs(sqft), 2)) != self.calcSqft(length, width, qty):
            raise serializers.ValidationError({"error" : "Final Inventory Item QTY_SQFT must be equal to (LENGTH x WIDTH / 144) x QTY"  ,   "error_ur" : "(LENGTH x WIDTH / 144) x QTY کے برابر ہونا چاہیے  QTY_SQFT فائنل انوینٹری آئٹم"  })
           
    def labourSqftCheck(self, finalSqft, labourSqft):
        if Decimal(abs(labourSqft)) > Decimal(abs(finalSqft)):
            raise serializers.ValidationError( {"error" : "Labour QTY_SQFT must be less than or equal to Final QTY_SQFT" ,   "error_ur" : " سے کم یا اس کے برابر ہونا چاہیے۔ QTY_SQFT فائنل QTY_SQFT لیبر  "    })
           
    def sectionedSqftCheck(self, totalInitialQty, totalFinalQty, iniQtyThickness, finalQtyThickness):
        wastedQty = abs(totalFinalQty) - abs(totalInitialQty)
        if Decimal(abs(finalQtyThickness + wastedQty)) > Decimal(abs(iniQtyThickness)):
            raise serializers.ValidationError( {"error" : "Initial (Qty x Thickness) must be greater than or equal to Final (Qty x Thickness) "   ,   "error_ur" : " سے زیادہ یا اس کے برابر ہونی چاہئے۔(مقدار x موٹائی) فائنل  (مقدار x موٹائی) ابتدائی" } )
           
    def nonSectionedSqftCheck(self, initialSqft, finalSqft):
        if Decimal(abs(finalSqft)) > Decimal(abs(initialSqft)):
            raise serializers.ValidationError(  {"error" : "Total Final Sqft must be equal to or less than Total initial sqft" ,   "error_ur" : "کل فائنل مربع فٹ کل ابتدائی مربع فٹ کے برابر یا اس سے کم ہونا چاہیے۔"  } )

    def validate(self, attrs):
        initial_inv = attrs.get('I_DETAILS')
        final_inv_list = attrs.get('F_DETAILS')
        inv_breakage = attrs.get('BREAKAGE')
        transaction_type = attrs.get('TRANS_TYP')
        labour_qty_sqft = attrs.get('LABOUR_SQFT')

        # check product in inv
        self.checkInitialProduct(
            typeOfTransac=transaction_type,
            initialProduct=initial_inv)

        iniProductSize = self.getProductSizeById(id=initial_inv["SIZE_ID"])
        self.initialSqftCheck(iniProductSize.LENGTH, iniProductSize.WIDTH,
                              initial_inv["QTY"], initial_inv["QTY_SQFT"])
        ini_qty_thickness = abs(initial_inv["QTY"]) * iniProductSize.THICKNESS

        total_final_sqft = abs(inv_breakage["AVLBL_SQFT"])
        final_qty_thickness = 0
        final_qty = 0

        for final_obj in final_inv_list:
            self.finalSqftCheck(
                final_obj["LENGTH"], final_obj["WIDTH"], final_obj["QTY"], final_obj["QTY_SQFT"])
            total_final_sqft += abs(final_obj["QTY_SQFT"])
            final_qty += abs(final_obj["QTY"])
            final_qty_thickness += (abs(final_obj["QTY"])
                                    * final_obj["THICKNESS"])

        if len(final_inv_list):
            self.labourSqftCheck(finalSqft=total_final_sqft,
                                 labourSqft=labour_qty_sqft)

        if transaction_type == "Sectioning":
            self.sectionedSqftCheck(
                totalInitialQty=initial_inv["QTY_SQFT"],
                totalFinalQty=final_qty,
                iniQtyThickness=ini_qty_thickness,
                finalQtyThickness=final_qty_thickness
            )
        else:
            self.nonSectionedSqftCheck(
                initialSqft=initial_inv["QTY_SQFT"],
                finalSqft=total_final_sqft
            )
        return attrs

    def create(self, validate_data):
        inv_detail_initial = validate_data.pop('I_DETAILS')
        inv_detail_final = validate_data.pop('F_DETAILS')
        inv_detail_final = validate_data.pop('BREAKAGE')

        if "TRANS_TYP" in validate_data:          
            TRANS_TYP = validate_data.pop('TRANS_TYP')
            convertFrom, convertTo = lang_detect(TRANS_TYP)
            validate_data["TRANS_TYP"], validate_data["TRANS_TYP_UR"]  = lang_translate(stringToConvert=TRANS_TYP, from_lang=convertFrom, to_lang=convertTo)

        created_inventory = Inventory_Transactions.objects.create(**validate_data)
        return created_inventory


    def update(self, instance, validated_data):
        inv_detail_initial = validated_data.pop('I_DETAILS')
        inv_detail_final = validated_data.pop('F_DETAILS')
        inv_detail_final = validated_data.pop('BREAKAGE')

        if "TRANS_TYP" in validated_data:          
            TRANS_TYP = validated_data.pop('TRANS_TYP')
            convertFrom, convertTo = lang_detect(TRANS_TYP)
            validated_data["TRANS_TYP"], validated_data["TRANS_TYP_UR"]  = lang_translate(stringToConvert=TRANS_TYP, from_lang=convertFrom, to_lang=convertTo)

        instance.TRANS_TYP = validated_data.get('TRANS_TYP', instance.TRANS_TYP)
        instance.TRANS_TYP_UR = validated_data.get('TRANS_TYP_UR', instance.TRANS_TYP_UR)

        instance.save()
        return instance

class DelInventorySerializer(serializers.ModelSerializer):

    TRANSC_DETALS = AddTransactionDetailsSerializer(read_only=True, many=True)

    class Meta:
        model = Inventory_Transactions
        fields = (
            'INV_TRANS_ID',
            'INVNTRY_DT',
            'TRANS_TYP',
            'LABOUR_COST',
            'LABOUR_SQFT',
            'LABOUR_RUN_FT',
            'TRANS_UNIT_COST',
            'ACCT_ID',
            'TRANSC_DETALS',
            'REC_ADD_DT',
            'REC_ADD_BY',
        )
