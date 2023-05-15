
from rest_framework import serializers
from django.db.models import Q
from inventory.model.Inventory import Inventory_Transactions
# models imports
from inventory.model.ProductInventory import ProductInventory
from inventory.model.Orders import Orders, Order_items
from logistics.model.Deliveries import Deliveries
# serialziers
from logistics.serializer.DeliveryItemsSerializer import DeliveryItemsSerializer, AddDeliveryItemSerializer
# Utils
from marble_erp.utils.langDetector import lang_detect
from marble_erp.utils.lang_translate import lang_translate


class AddDeliverySerializer(serializers.ModelSerializer):
    DELIVERY_ITEMS = AddDeliveryItemSerializer(many=True)

    class Meta:
        model = Deliveries
        fields = '__all__'
    # create and update


    def checkOrderExist(self, orderId, merchant=None, customer=None):
        try:
            if merchant:
                order_qs = Orders.objects.get(
                    MRCHNT_ACCT_ID__ACCT_ID=merchant.ACCT_ID, ORDR_ID=orderId.ORDR_ID)
            if customer:
                order_qs = Orders.objects.get(
                    CUST_ACCT_ID__ACCT_ID=customer.ACCT_ID, ORDR_ID=orderId.ORDR_ID)
        except:
            raise serializers.ValidationError( {'error': 'Customer/Merchant order doess not exist'  , 'error_ur': 'کسٹمر/مرچنٹ آرڈر موجود نہیں ہے۔'})
        return order_qs

    def checkOrderItemQty(self, index, orderId, orderItemId, orderItemQty = 0, isReturnDelivery = 0):
        try:
            orderItem = Order_items.objects.get(
                ORDR_ITEM_ID=orderItemId, ORDR_ID=orderId)
        except:
            raise serializers.ValidationError( {'error': "Customer/Merchant order item {0} does not exist".format(index)  , 'error_ur':  "کسٹمر/مرچنٹ آرڈر آئٹم موجود نہیں ہے۔ {0}".format(index)    }) 
        if isReturnDelivery == 1:
            if -(orderItemQty) > orderItem.DLVRD_QTY or orderItemQty >= 0:
                raise serializers.ValidationError( {'error': "Item {0} : Delivery Qty cannot exceed Deliverd Qty".format(index)  , 'error_ur':  "آئٹم کی ترسیل کی مقدار ڈیلیوری کی مقدار سے زیادہ نہیں ہو سکتی : {0} " .format(index)    }) 
        else:
            remaingQty = orderItem.REQ_QTY - orderItem.DLVRD_QTY
            if remaingQty < orderItemQty:
                raise serializers.ValidationError( {'error': "Item {0}:  Delivery Qty cannot exceed Order Qty".format(index)  , 'error_ur':  "آئٹم کی ترسیل کی مقدار آرڈر کی مقدار سے زیادہ نہیں ہو سکتی : {0}".format(index)    }) 

        return orderItem
        

    def checkQtyInInventory(self, delivery, order_item, deliveryItemQty):
        if delivery.get("IS_SALE") == 1:
            try:
                inv_product = ProductInventory.objects.get(PROD_ID=order_item.PRODUCT_ID.PRODUCT_ID, SIZE_ID=order_item.DLVRY_SIZE_ID.SIZE_ID, IS_SIZED=order_item.IS_SIZED,
                                                           IS_SECTIONED=order_item.IS_SECTIONED, IS_GOLA=order_item.IS_GOLA, IS_POLISHED=order_item.IS_POLISHED, IS_AVLBL=1)
            except ProductInventory.DoesNotExist:
                raise serializers.ValidationError( 
                    {'error': 'Customer/Merchant delivery item does not exist in inventory'  
                    , 'error_ur': 'گاہک/مرچنٹ ڈیلیوری آئٹم انوینٹری میں موجود نہیں ہے۔'}

                )
            if inv_product.AVLBL_QTY < deliveryItemQty:
                raise serializers.ValidationError( {'error': 'Delivery Quantity cannot exceed Inventory Quantity'  , 'error_ur': 'ڈیلیوری کی مقدار انوینٹری کی مقدار سے زیادہ نہیں ہو سکتی'  })

    def validate(self, attrs):
        deliveryAttr = attrs
        delivery_item_list = attrs.get('DELIVERY_ITEMS')
        order_id = attrs.get("ORDR_ID")
        merchantAcct = attrs.get("MRCHNT_ACCT_ID", '')
        customerAcct = attrs.get("CUST_ACCT_ID", '')
        is_return = attrs.get("IS_RETURN", 0)
        # Account Checks
        if deliveryAttr.get("IS_SALE") == 1 and deliveryAttr.get("CUST_ACCT_ID") is None:
            raise serializers.ValidationError( {'error': 'Customer is required field.'  , 'error_ur': 'گاہک کو فیلڈ کی ضرورت ہے۔'  })
        elif  deliveryAttr.get("IS_SALE") == 0 and deliveryAttr.get("MRCHNT_ACCT_ID") is None:
            raise serializers.ValidationError( {'error': 'Merchant is required field.'  , 'error_ur': 'مرچنٹ کو فیلڈ درکار ہے۔'  })
        # Order Existance Check
        order = self.checkOrderExist(
            merchant=merchantAcct, customer=customerAcct, orderId=order_id)
        counter = 0
        for deliveryItem in delivery_item_list:
            counter = counter + 1
            # Order Qty Check
            orderItem = self.checkOrderItemQty(
                index=counter,
                orderId=order.ORDR_ID,
                orderItemId=deliveryItem.get(
                    "ORDR_ITEM_ID").ORDR_ITEM_ID,
                orderItemQty=deliveryItem.get("PROD_QTY"),
                isReturnDelivery=is_return)
            
        return attrs

    def create(self, validate_data):
        delivery_items = validate_data.pop('DELIVERY_ITEMS')

        if "SRC_ADDR" in validate_data and  len(validate_data["SRC_ADDR"])>0:    
            SRC_ADDR = validate_data.pop('SRC_ADDR')
            convertFrom, convertTo = lang_detect(SRC_ADDR)
            validate_data["SRC_ADDR"], validate_data["SRC_ADDR_UR"]  = lang_translate(stringToConvert=SRC_ADDR, from_lang=convertFrom, to_lang=convertTo)
        
        if "DESTNTN_ADDR" in validate_data and  len(validate_data["DESTNTN_ADDR"])>0:    
            DESTNTN_ADDR = validate_data.pop('DESTNTN_ADDR')
            convertFrom, convertTo = lang_detect(DESTNTN_ADDR)
            validate_data["DESTNTN_ADDR"], validate_data["DESTNTN_ADDR_UR"]  = lang_translate(stringToConvert=DESTNTN_ADDR, from_lang=convertFrom, to_lang=convertTo)
         
        if "DLVRY_DRIVER" in validate_data and  len(validate_data["DLVRY_DRIVER"])>0:    
            DLVRY_DRIVER = validate_data.pop('DLVRY_DRIVER')
            convertFrom, convertTo = lang_detect(DLVRY_DRIVER)
            validate_data["DLVRY_DRIVER"], validate_data["DLVRY_DRIVER_UR"]  = lang_translate(stringToConvert=DLVRY_DRIVER, from_lang=convertFrom, to_lang=convertTo)
        
        if "DLVRY_VHICLE" in validate_data and  len(validate_data["DLVRY_VHICLE"])>0:    
            DLVRY_VHICLE = validate_data.pop('DLVRY_VHICLE')
            convertFrom, convertTo = lang_detect(DLVRY_VHICLE)
            validate_data["DLVRY_VHICLE"], validate_data["DLVRY_VHICLE_UR"]  = lang_translate(stringToConvert=DLVRY_VHICLE, from_lang=convertFrom, to_lang=convertTo)
        
        if "DLVRY_DETAIL" in validate_data and  len(validate_data["DLVRY_DETAIL"])>0:    
            DLVRY_DETAIL = validate_data.pop('DLVRY_DETAIL')
            convertFrom, convertTo = lang_detect(DLVRY_DETAIL)
            validate_data["DLVRY_DETAIL"], validate_data["DLVRY_DETAIL_UR"]  = lang_translate(stringToConvert=DLVRY_DETAIL, from_lang=convertFrom, to_lang=convertTo)
        
        created_inventory = Deliveries.objects.create(**validate_data)
        return created_inventory

    def update(self, instance, validated_data):
        delivery_items = validated_data.pop('DELIVERY_ITEMS')

        if "SRC_ADDR" in validated_data and  len(validated_data["SRC_ADDR"])>0:    
            SRC_ADDR = validated_data.pop('SRC_ADDR')
            convertFrom, convertTo = lang_detect(SRC_ADDR)
            validated_data["SRC_ADDR"], validated_data["SRC_ADDR_UR"]  = lang_translate(stringToConvert=SRC_ADDR, from_lang=convertFrom, to_lang=convertTo)
        
        if "DESTNTN_ADDR" in validated_data and  len(validated_data["DESTNTN_ADDR"])>0:    
            DESTNTN_ADDR = validated_data.pop('DESTNTN_ADDR')
            convertFrom, convertTo = lang_detect(DESTNTN_ADDR)
            validated_data["DESTNTN_ADDR"], validated_data["DESTNTN_ADDR_UR"]  = lang_translate(stringToConvert=DESTNTN_ADDR, from_lang=convertFrom, to_lang=convertTo)
         
        if "DLVRY_DRIVER" in validated_data and  len(validated_data["DLVRY_DRIVER"])>0:    
            DLVRY_DRIVER = validated_data.pop('DLVRY_DRIVER')
            convertFrom, convertTo = lang_detect(DLVRY_DRIVER)
            validated_data["DLVRY_DRIVER"], validated_data["DLVRY_DRIVER_UR"]  = lang_translate(stringToConvert=DLVRY_DRIVER, from_lang=convertFrom, to_lang=convertTo)
        
        if "DLVRY_VHICLE" in validated_data and  len(validated_data["DLVRY_VHICLE"])>0:    
            DLVRY_VHICLE = validated_data.pop('DLVRY_VHICLE')
            convertFrom, convertTo = lang_detect(DLVRY_VHICLE)
            validated_data["DLVRY_VHICLE"], validated_data["DLVRY_VHICLE_UR"]  = lang_translate(stringToConvert=DLVRY_VHICLE, from_lang=convertFrom, to_lang=convertTo)
        
        if "DLVRY_DETAIL" in validated_data and  len(validated_data["DLVRY_DETAIL"])>0:    
            DLVRY_DETAIL = validated_data.pop('DLVRY_DETAIL')
            convertFrom, convertTo = lang_detect(DLVRY_DETAIL)
            validated_data["DLVRY_DETAIL"], validated_data["DLVRY_DETAIL_UR"]  = lang_translate(stringToConvert=DLVRY_DETAIL, from_lang=convertFrom, to_lang=convertTo)
         
        instance.IS_SALE = validated_data.get('IS_SALE', instance.IS_SALE)
        instance.DLVRY_DT = validated_data.get('DLVRY_DT', instance.DLVRY_DT)
        instance.IS_RETURN = validated_data.get('IS_RETURN', instance.IS_RETURN)
        instance.SRC_ADDR = validated_data.get('SRC_ADDR', instance.SRC_ADDR)
        instance.DESTNTN_ADDR = validated_data.get('DESTNTN_ADDR', instance.DESTNTN_ADDR)
        instance.DLVRY_DRIVER = validated_data.get('DLVRY_DRIVER', instance.DLVRY_DRIVER)
        instance.DLVRY_VHICLE = validated_data.get('DLVRY_VHICLE', instance.DLVRY_VHICLE)
        instance.DLVRY_DETAIL = validated_data.get('DLVRY_DETAIL', instance.DLVRY_DETAIL)
        instance.SRC_ADDR_UR = validated_data.get('SRC_ADDR_UR', instance.SRC_ADDR_UR)
        instance.DESTNTN_ADDR_UR = validated_data.get('DESTNTN_ADDR_UR', instance.DESTNTN_ADDR_UR)
        instance.DLVRY_DRIVER_UR = validated_data.get('DLVRY_DRIVER_UR', instance.DLVRY_DRIVER_UR)
        instance.DLVRY_VHICLE_UR = validated_data.get('DLVRY_VHICLE_UR', instance.DLVRY_VHICLE_UR)
        instance.DLVRY_DETAIL_UR = validated_data.get('DLVRY_DETAIL_UR', instance.DLVRY_DETAIL_UR)
        instance.IS_ACTIVE = validated_data.get('IS_ACTIVE', instance.IS_ACTIVE)
        # if instance.IS_RETURN:
        instance.LOAD_COST = validated_data.get('LOAD_COST', instance.LOAD_COST)
        instance.RENT_COST = validated_data.get('RENT_COST', instance.RENT_COST)
        instance.EXTRAS_COST = validated_data.get('EXTRAS_COST', instance.EXTRAS_COST)
        instance.DLVRY_COST = validated_data.get('DLVRY_COST', instance.DLVRY_COST)
        instance.CUST_ACCT_ID = validated_data.get('CUST_ACCT_ID', instance.CUST_ACCT_ID)
        instance.MRCHNT_ACCT_ID = validated_data.get('MRCHNT_ACCT_ID', instance.MRCHNT_ACCT_ID)
        instance.DLVRY_BY_EMP_ID = validated_data.get('DLVRY_BY_EMP_ID', instance.DLVRY_BY_EMP_ID)
        instance.ORDR_ID = validated_data.get('ORDR_ID', instance.ORDR_ID)
        instance.REC_MOD_BY = validated_data.get('REC_MOD_BY', instance.REC_MOD_BY)
        instance.save()
        return instance


class DeliveriesDetailSerializer(serializers.ModelSerializer):
    DELIVERY_ITEMS = DeliveryItemsSerializer(read_only=True, many=True)

    class Meta:
        model = Deliveries
        fields = '__all__'
        # depth = 1
