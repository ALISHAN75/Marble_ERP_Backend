from rest_framework import serializers
# models imports
from finance.model.Expense_Transactions import Expense_Transactions
from finance.serializer.ExpenseTransItemsSerializer import ExpenseTransItemsSerializer
# Utils
from marble_erp.utils.langDetector import lang_detect
from marble_erp.utils.lang_translate import lang_translate

class ExpenseTransSerializer(serializers.ModelSerializer):
    EXPNS_TRANS_ITEMS = ExpenseTransItemsSerializer(many=True)

    class Meta:
        model = Expense_Transactions
        fields =  '__all__'
        extra_kwargs = {'PAYMNT_DT': {'required': True} , 
                        'EXPNS_TYP_ACCT': {'required': True} ,
                        'ACCT_ID': {'required': True} ,
                        'PYMNT_BY_EMP_ID': {'required': True} ,
                        'TOTAL_wTAX': {'required': True} ,
                        'TOTAL_noTAX': {'required': True} ,
                        }

        
    def create(self, validate_data):
        EXPNS_TRANS_ITEMS = validate_data.pop('EXPNS_TRANS_ITEMS')
        if "PYMENT_TO" in validate_data and  len(validate_data["PYMENT_TO"])>0:  
            PYMENT_TO = validate_data.pop('PYMENT_TO')
            convertFrom, convertTo = lang_detect(PYMENT_TO)
            validate_data["PYMENT_TO"], validate_data["PYMENT_TO_UR"]  = lang_translate(stringToConvert=PYMENT_TO, from_lang=convertFrom, to_lang=convertTo)
        if "NOTES" in validate_data and  len(validate_data["NOTES"])>0:         
            NOTES = validate_data.pop('NOTES')
            convertFrom, convertTo = lang_detect(NOTES)
            validate_data["NOTES"], validate_data["NOTES_UR"]  = lang_translate(stringToConvert=NOTES, from_lang=convertFrom, to_lang=convertTo)
     
        created_exp = Expense_Transactions.objects.create(**validate_data)
        return created_exp
    


class DetailedExpenseTransSerializer(serializers.ModelSerializer):
    EXPNS_TRANS_ITEMS = ExpenseTransItemsSerializer(many=True)

    class Meta:
        model = Expense_Transactions
        fields =  '__all__'
        depth = 2



class AdvanceExpenseTransSerializer(serializers.ModelSerializer):

    class Meta:
        model = Expense_Transactions
        fields =  '__all__'
        extra_kwargs = {'PAYMNT_DT': {'required': True} , 
                        'EXPNS_TYP_ACCT': {'required': True} ,
                        'ACCT_ID': {'required': True} ,
                        'PYMNT_BY_EMP_ID': {'required': True} ,
                        'TOTAL_wTAX': {'required': True} ,
                        'TOTAL_noTAX': {'required': True} ,
                        }
                        
    def create(self, validate_data):
        if "PYMENT_TO" in validate_data and  len(validate_data["PYMENT_TO"])>0:  
            PYMENT_TO = validate_data.pop('PYMENT_TO')
            convertFrom, convertTo = lang_detect(PYMENT_TO)
            validate_data["PYMENT_TO"], validate_data["PYMENT_TO_UR"]  = lang_translate(stringToConvert=PYMENT_TO, from_lang=convertFrom, to_lang=convertTo)
        if "NOTES" in validate_data and  len(validate_data["NOTES"])>0:         
            NOTES = validate_data.pop('NOTES')
            convertFrom, convertTo = lang_detect(NOTES)
            validate_data["NOTES"], validate_data["NOTES_UR"]  = lang_translate(stringToConvert=NOTES, from_lang=convertFrom, to_lang=convertTo)
     
        created_exp = Expense_Transactions.objects.create(**validate_data)
        return created_exp

class AdddExpenseTransSerializer(serializers.ModelSerializer):

    class Meta:
        model = Expense_Transactions
        fields =  '__all__'
                        
    def create(self, validate_data):
        if "PYMENT_TO" in validate_data and  len(validate_data["PYMENT_TO"])>0:  
            PYMENT_TO = validate_data.pop('PYMENT_TO')
            convertFrom, convertTo = lang_detect(PYMENT_TO)
            validate_data["PYMENT_TO"], validate_data["PYMENT_TO_UR"]  = lang_translate(stringToConvert=PYMENT_TO, from_lang=convertFrom, to_lang=convertTo)
        if "NOTES" in validate_data and  len(validate_data["NOTES"])>0:         
            NOTES = validate_data.pop('NOTES')
            convertFrom, convertTo = lang_detect(NOTES)
            validate_data["NOTES"], validate_data["NOTES_UR"]  = lang_translate(stringToConvert=NOTES, from_lang=convertFrom, to_lang=convertTo)
     
        created_exp = Expense_Transactions.objects.create(**validate_data)
        return created_exp



        