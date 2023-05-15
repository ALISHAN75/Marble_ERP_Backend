from rest_framework import serializers
# models imports
from finance.model.Expense_Transactions import Expense_Transaction_Items
# Utils
from marble_erp.utils.langDetector import lang_detect
from marble_erp.utils.lang_translate import lang_translate

class ExpenseTransItemsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Expense_Transaction_Items
        fields = '__all__'
        
    def create(self, validate_data):
        ITEM_NM = validate_data.pop('ITEM_NM')
        convertFrom, convertTo = lang_detect(ITEM_NM)
        validate_data["ITEM_NM"], validate_data["ITEM_NM_UR"]  = lang_translate(stringToConvert=ITEM_NM, from_lang=convertFrom, to_lang=convertTo)
        if "ITEM_DESC" in validate_data:          
            ITEM_DESC = validate_data.pop('ITEM_DESC')
            convertFrom, convertTo = lang_detect(ITEM_DESC)
            validate_data["ITEM_DESC"], validate_data["ITEM_DESC_UR"]  = lang_translate(stringToConvert=ITEM_DESC, from_lang=convertFrom, to_lang=convertTo)

     
        created_exp = Expense_Transaction_Items.objects.create(**validate_data)
        return created_exp
