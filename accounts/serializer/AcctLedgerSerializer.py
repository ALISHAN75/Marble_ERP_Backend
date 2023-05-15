from rest_framework import serializers
# models
from accounts.model.AcctLedger import Acct_Ledger
# serialzier
from accounts.serializer.UsersSerializer import AccountsSerializer
from accounts.serializer.UsersSerializer import AccountsSerializer
# Utils
from marble_erp.utils.langDetector import lang_detect
from marble_erp.utils.lang_translate import lang_translate


class AcctLedgerSerializer(serializers.ModelSerializer):

  class Meta:
    model = Acct_Ledger
    fields = (
      'ID',
      'ACCT_ID',
      'ORDINAL',
      'TRANSC_DESC',
      'TRANSC_DESC_UR',
      'EARN_TRANS_ID',
      'EXPNS_TRANS_ID',
      'EARNING',
      'EXPENSE',
      'BALANCE',
      'REC_ADD_DT',
      'REC_ADD_BY',
    )
    depth=1


class AddAcctLedgerSerializer(serializers.ModelSerializer):

  class Meta:
    model = Acct_Ledger
    fields = '__all__'
    

  def create(self, validate_data):
        if "TRANSC_DESC" in validate_data: 
          TRANSC_DESC = validate_data.pop('TRANSC_DESC')
          convertFrom, convertTo = lang_detect(TRANSC_DESC)
          validate_data["TRANSC_DESC"], validate_data["TRANSC_DESC_UR"]  = lang_translate(stringToConvert=TRANSC_DESC, from_lang=convertFrom, to_lang=convertTo)
     
        created_acct = Acct_Ledger.objects.create(**validate_data)
        return created_acct

  def update(self, instance, validated_data):     
        if "TRANSC_DESC" in validated_data: 
          TRANSC_DESC = validated_data.pop('TRANSC_DESC')
          convertFrom, convertTo = lang_detect(TRANSC_DESC)
          validated_data["TRANSC_DESC"], validated_data["TRANSC_DESC_UR"]  = lang_translate(stringToConvert=TRANSC_DESC, from_lang=convertFrom, to_lang=convertTo)
     
        instance.ORDINAL = validated_data.get('ORDINAL', instance.ORDINAL)
        instance.TRANSC_DESC = validated_data.get('TRANSC_DESC', instance.TRANSC_DESC)
        instance.TRANSC_DESC_UR = validated_data.get('TRANSC_DESC_UR', instance.TRANSC_DESC_UR)
        instance.EARNING = validated_data.get('EARNING', instance.EARNING)
        instance.EXPENSE = validated_data.get('EXPENSE', instance.EXPENSE)   
        instance.BALANCE = validated_data.get('BALANCE', instance.BALANCE)
        instance.REC_ADD_DT = validated_data.get('REC_ADD_DT', instance.REC_ADD_DT)
        instance.REC_ADD_BY = validated_data.get('REC_ADD_BY', instance.REC_ADD_BY)
        instance.ACCT_ID = validated_data.get('ACCT_ID', instance.ACCT_ID)
        instance.EARN_TRANS_ID = validated_data.get('EARN_TRANS_ID', instance.EARN_TRANS_ID)
        instance.EXPNS_TRANS_ID = validated_data.get('EXPNS_TRANS_ID', instance.EXPNS_TRANS_ID)

        instance.save()
        return instance
  

