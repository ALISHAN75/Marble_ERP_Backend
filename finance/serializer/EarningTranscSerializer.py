from rest_framework import serializers
# models imports
from finance.model.Earning_Transactions import Earning_Transactions
from finance.model.Earning_Transactions import Earning_Transactions
from finance.serializer.EarningTransItemsSerializer import EarningTransItemsSerializer
# Utils
from marble_erp.utils.langDetector import lang_detect
from marble_erp.utils.lang_translate import lang_translate

class EarningTranscSerializer(serializers.ModelSerializer):
    EARNS_TRANS_ITEMS = EarningTransItemsSerializer(many=True)

    class Meta:
        model = Earning_Transactions
        fields =  '__all__'
        extra_kwargs = {'PYMNT_DT': {'required': True} , 
                        'EARN_TYP_ACCT': {'required': True} ,
                        'ACCT_ID': {'required': True} ,
                        'EMP_ID': {'required': True} ,
                        'PYMNT_AMNT': {'required': True} ,
                        'PYMNT_BY': {'required': True} , 
                        }
        
    def create(self, validate_data):
        EXPNS_TRANS_ITEMS = validate_data.pop('EARNS_TRANS_ITEMS')
        if "PYMNT_BY" in validate_data  and  len(validate_data["PYMNT_BY"])>0:
            PYMNT_BY = validate_data.pop('PYMNT_BY')
            convertFrom, convertTo = lang_detect(PYMNT_BY)
            validate_data["PYMNT_BY"], validate_data["PYMNT_BY_UR"]  = lang_translate(stringToConvert=PYMNT_BY, from_lang=convertFrom, to_lang=convertTo)
        if "NOTES" in validate_data   and  len(validate_data["NOTES"])>0:          
            NOTES = validate_data.pop('NOTES')
            convertFrom, convertTo = lang_detect(NOTES)
            validate_data["NOTES"], validate_data["NOTES_UR"]  = lang_translate(stringToConvert=NOTES, from_lang=convertFrom, to_lang=convertTo)
     
        created_earn = Earning_Transactions.objects.create(**validate_data)
        return created_earn


class SecondEarningTranscSerializer(serializers.ModelSerializer):
    EARNS_TRANS_ITEMS = EarningTransItemsSerializer(many=True)

    class Meta:
        model = Earning_Transactions
        fields =  '__all__'
        extra_kwargs = {'PYMNT_DT': {'required': True} , 
                        'EARN_TYP_ACCT': {'required': True} ,
                        'ACCT_ID': {'required': True} ,
                        'EMP_ID': {'required': True} ,
                        'PYMNT_AMNT': {'required': True} 
                        }
        
    def create(self, validate_data):
        EARNS_TRANS_ITEMS = validate_data.pop('EARNS_TRANS_ITEMS')
        if "PYMNT_BY" in validate_data  and  len(validate_data["PYMNT_BY"])>0:
            PYMNT_BY = validate_data.pop('PYMNT_BY')
            convertFrom, convertTo = lang_detect(PYMNT_BY)
            validate_data["PYMNT_BY"], validate_data["PYMNT_BY_UR"]  = lang_translate(stringToConvert=PYMNT_BY, from_lang=convertFrom, to_lang=convertTo)
        if "NOTES" in validate_data   and  len(validate_data["NOTES"])>0:          
            NOTES = validate_data.pop('NOTES')
            convertFrom, convertTo = lang_detect(NOTES)
            validate_data["NOTES"], validate_data["NOTES_UR"]  = lang_translate(stringToConvert=NOTES, from_lang=convertFrom, to_lang=convertTo)
     
        created_earn = Earning_Transactions.objects.create(**validate_data)
        return created_earn


class DetailedEarningTranscSerializer(serializers.ModelSerializer):
    EARNS_TRANS_ITEMS = EarningTransItemsSerializer(many=True)

    class Meta:
        model = Earning_Transactions
        fields = "__all__"
        depth = 2


class AddEarningTranscSerializer(serializers.ModelSerializer):

    class Meta:
        model = Earning_Transactions
        fields =  '__all__'

    def create(self, validate_data):
        if "PYMNT_BY" in validate_data  and  len(validate_data["PYMNT_BY"])>0:
            PYMNT_BY = validate_data.pop('PYMNT_BY')
            convertFrom, convertTo = lang_detect(PYMNT_BY)
            validate_data["PYMNT_BY"], validate_data["PYMNT_BY_UR"]  = lang_translate(stringToConvert=PYMNT_BY, from_lang=convertFrom, to_lang=convertTo)
        if "NOTES" in validate_data   and  len(validate_data["NOTES"])>0:          
            NOTES = validate_data.pop('NOTES')
            convertFrom, convertTo = lang_detect(NOTES)
            validate_data["NOTES"], validate_data["NOTES_UR"]  = lang_translate(stringToConvert=NOTES, from_lang=convertFrom, to_lang=convertTo)
     
        created_earn = Earning_Transactions.objects.create(**validate_data)
        return created_earn

    def update(self, instance, validated_data):     
        if "PYMNT_BY" in validated_data  and  len(validated_data["PYMNT_BY"])>0:
            PYMNT_BY = validated_data.pop('PYMNT_BY')
            convertFrom, convertTo = lang_detect(PYMNT_BY)
            validated_data["PYMNT_BY"], validated_data["PYMNT_BY_UR"]  = lang_translate(stringToConvert=PYMNT_BY, from_lang=convertFrom, to_lang=convertTo)
        if "NOTES" in validated_data   and  len(validated_data["NOTES"])>0:          
            NOTES = validated_data.pop('NOTES')
            convertFrom, convertTo = lang_detect(NOTES)
            validated_data["NOTES"], validated_data["NOTES_UR"]  = lang_translate(stringToConvert=NOTES, from_lang=convertFrom, to_lang=convertTo)
     
        instance.PYMNT_BY = validated_data.get('PYMNT_BY', instance.PYMNT_BY)
        instance.PYMNT_BY_UR = validated_data.get('PYMNT_BY_UR', instance.PYMNT_BY_UR)
        instance.PYMNT_AMNT = validated_data.get('PYMNT_AMNT', instance.PYMNT_AMNT)
        instance.PYMNT_DT = validated_data.get('PYMNT_DT', instance.PYMNT_DT)
        instance.IS_CASH = validated_data.get('IS_CASH', instance.IS_CASH)   
        instance.NOTES = validated_data.get('NOTES', instance.NOTES)
        instance.NOTES_UR = validated_data.get('NOTES_UR', instance.NOTES_UR)
        instance.REC_ADD_DT = validated_data.get('REC_ADD_DT', instance.REC_ADD_DT)
        instance.REC_ADD_BY = validated_data.get('REC_ADD_BY', instance.REC_ADD_BY)
        instance.ACCT_ID = validated_data.get('ACCT_ID', instance.ACCT_ID)
        instance.DLVRY_ID = validated_data.get('DLVRY_ID', instance.DLVRY_ID)
        instance.EMP_ID = validated_data.get('EMP_ID', instance.EMP_ID)
        instance.INVNTRY_TRANS_ID = validated_data.get('INVNTRY_TRANS_ID', instance.INVNTRY_TRANS_ID)
        instance.EARN_TYP_ACCT = validated_data.get('EARN_TYP_ACCT', instance.EARN_TYP_ACCT)

        instance.save()
        return instance

        
class AdvanceEarningTranscSerializer(serializers.ModelSerializer):

    class Meta:
        model = Earning_Transactions
        fields =  '__all__'
        extra_kwargs = {'PYMNT_DT': {'required': True} , 
                        'EARN_TYP_ACCT': {'required': True} ,
                        'ACCT_ID': {'required': True} ,
                        'EMP_ID': {'required': True} ,
                        'PYMNT_AMNT': {'required': True} , 
                        'PYMNT_BY': {'required': True} , 
                        }

    def create(self, validate_data):
        if "PYMNT_BY" in validate_data  and  len(validate_data["PYMNT_BY"])>0:
            PYMNT_BY = validate_data.pop('PYMNT_BY')
            convertFrom, convertTo = lang_detect(PYMNT_BY)
            validate_data["PYMNT_BY"], validate_data["PYMNT_BY_UR"]  = lang_translate(stringToConvert=PYMNT_BY, from_lang=convertFrom, to_lang=convertTo)
        if "NOTES" in validate_data   and  len(validate_data["NOTES"])>0:          
            NOTES = validate_data.pop('NOTES')
            convertFrom, convertTo = lang_detect(NOTES)
            validate_data["NOTES"], validate_data["NOTES_UR"]  = lang_translate(stringToConvert=NOTES, from_lang=convertFrom, to_lang=convertTo)
     
        created_earn = Earning_Transactions.objects.create(**validate_data)
        return created_earn

class SecondAdvanceEarningTranscSerializer(serializers.ModelSerializer):

    class Meta:
        model = Earning_Transactions
        fields =  '__all__'
        extra_kwargs = {'PYMNT_DT': {'required': True} , 
                        'EARN_TYP_ACCT': {'required': True} ,
                        'ACCT_ID': {'required': True} ,
                        'EMP_ID': {'required': True} ,
                        'PYMNT_AMNT': {'required': True} 
                        }

    def create(self, validate_data):
        if "PYMNT_BY" in validate_data  and  len(validate_data["PYMNT_BY"])>0:
            PYMNT_BY = validate_data.pop('PYMNT_BY')
            convertFrom, convertTo = lang_detect(PYMNT_BY)
            validate_data["PYMNT_BY"], validate_data["PYMNT_BY_UR"]  = lang_translate(stringToConvert=PYMNT_BY, from_lang=convertFrom, to_lang=convertTo)
        if "NOTES" in validate_data   and  len(validate_data["NOTES"])>0:          
            NOTES = validate_data.pop('NOTES')
            convertFrom, convertTo = lang_detect(NOTES)
            validate_data["NOTES"], validate_data["NOTES_UR"]  = lang_translate(stringToConvert=NOTES, from_lang=convertFrom, to_lang=convertTo)
     
        created_earn = Earning_Transactions.objects.create(**validate_data)
        return created_earn
