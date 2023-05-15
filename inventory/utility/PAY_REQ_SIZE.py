# models imports 
from inventory.model.ProductCategory import  ProductCategory
from inventory.model.ProductName import  ProductName
from inventory.model.Products import  Products
from inventory.model.ProductSizes import ProductSizes
from inventory.model.UsageType import UsageType
# serializers imports
from inventory.serializers.ProductSizesSerializer import ProductSizesSerializer
from inventory.serializers.ProductCategorySerializer import ProductCategorySerializer
from inventory.serializers.ProductNameSerializer import ProductNameSerializer
from inventory.serializers.ProductsSerializer import ProductsSerializer
from inventory.serializers.UsageTypeSerializer import UsageTypeSerializer
# Utils
from marble_erp.utils.langDetector import lang_detect
from marble_erp.utils.lang_translate import lang_translate


# Saving the PAY_REQ_SIZE
def pay_Size(THICKNESS, WIDTH,LENGTH,ID ):
    try:
        ProductSize =  ProductSizes.objects.get(THICKNESS=THICKNESS, WIDTH=WIDTH ,LENGTH = LENGTH)
        return ProductSize.SIZE_ID        
    except ProductSizes.DoesNotExist:
        PRDCT_SIZE = {
            'WIDTH'  :WIDTH,
            'LENGTH'  :LENGTH,
            'THICKNESS'  :THICKNESS,
            'REC_ADD_BY' : ID,
            'REC_MOD_BY' : ID
             }
        create_serializer = ProductSizesSerializer(data=PRDCT_SIZE)
        if create_serializer.is_valid():
            new_product_size = create_serializer.save()
            return  new_product_size.SIZE_ID 

# Saving the PRODUCT_CATEGORY
def product_Category(CAT_NAME,ID ):
    convertFrom, convertTo = lang_detect(CAT_NAME)
    try:
        if convertFrom == 'en':
            Productcategory =  ProductCategory.objects.get(CAT_NM=CAT_NAME)
        elif convertFrom == 'ur':
            Productcategory =  ProductCategory.objects.get(CAT_NM_UR=CAT_NAME)
        return Productcategory.CAT_ID        
    except ProductCategory.DoesNotExist:
        
        PRDCT_CAT = {
            'IS_ACTIVE'  :1,
            'REC_ADD_BY' : ID,
            'REC_MOD_BY' : ID
             }
        PRDCT_CAT["CAT_NM"], PRDCT_CAT["CAT_NM_UR"]  = lang_translate(stringToConvert=CAT_NAME, from_lang=convertFrom, to_lang=convertTo)
        create_serializer = ProductCategorySerializer(data=PRDCT_CAT)
        if create_serializer.is_valid():
            new_product_size = create_serializer.save()
            return  new_product_size.CAT_ID 


# Saving the PRODUCT_CATEGORY
def product_Name(PRO_NAME,ID ):
    convertFrom, convertTo = lang_detect(PRO_NAME)
    try:
        if convertFrom == 'en':
            Productname =  ProductName.objects.get(PROD_NM=PRO_NAME)
        elif convertFrom == 'ur':
            Productname =  ProductName.objects.get(PROD_NM_UR=PRO_NAME)
        return Productname.PROD_NM_ID        
    except ProductName.DoesNotExist:
        PRDCT_NAME = {
            'IS_ACTIVE'  :1,
            'REC_ADD_BY' : ID,
            'REC_MOD_BY' : ID
             }
        PRDCT_NAME["PROD_NM"], PRDCT_NAME["PROD_NM_UR"]  = lang_translate(stringToConvert=PRO_NAME, from_lang=convertFrom, to_lang=convertTo)
        create_serializer = ProductNameSerializer(data=PRDCT_NAME)
        if create_serializer.is_valid():
            new_product_size = create_serializer.save()
            return  new_product_size.PROD_NM_ID 



# Saving the PRODUCT_USAGE
def product_Usage(PRO_USAGE,ID ):
    convertFrom, convertTo = lang_detect(PRO_USAGE)
    try:
        if convertFrom == 'en':
            Productusage =  UsageType.objects.get(USAGE_NM  =PRO_USAGE)
        elif convertFrom == 'ur':
            Productusage =  UsageType.objects.get(USAGE_NM_UR  =PRO_USAGE)

        return Productusage.USAGE_ID        
    except UsageType.DoesNotExist:
        PRDCT_USAGE = {
            'IS_ACTIVE'  :1,
            'REC_ADD_BY' : ID,
            'REC_MOD_BY' : ID
             }       
        PRDCT_USAGE["USAGE_NM"], PRDCT_USAGE["USAGE_NM_UR"]  = lang_translate(stringToConvert=PRO_USAGE, from_lang=convertFrom, to_lang=convertTo)
        create_serializer = UsageTypeSerializer(data=PRDCT_USAGE)
        if create_serializer.is_valid():
            new_product_size = create_serializer.save()
            return  new_product_size.USAGE_ID 


# Saving the PRODUCT
def PRODUCT(CAT_NAME,PPRO_NAME,PRO_USAGE,ID ):
    try:
        Product =  Products.objects.get(PROD_NM_ID=product_Name(PPRO_NAME , ID),CAT_ID=product_Category(CAT_NAME , ID),USAGE_ID=product_Usage(PRO_USAGE,ID))
        return Product.PRODUCT_ID        
    except Products.DoesNotExist:
        PRDCT = {
            'PROD_NM_ID':product_Name(PPRO_NAME , ID),
            'CAT_ID' : product_Category(CAT_NAME , ID),
            'USAGE_ID':product_Usage(PRO_USAGE,ID),
            'PROD_AVLBL_QTY'  :00.00,
            'IS_ACTIVE'  :1,
            'REC_ADD_BY' : ID,
            'REC_MOD_BY' : ID
             }
        create_serializer = ProductsSerializer(data=PRDCT)
        if create_serializer.is_valid():
            new_product_size = create_serializer.save()
            return  new_product_size.PRODUCT_ID 
