from rest_framework import serializers
# models
from accounts.model.CashLedger import CashLedger
# Utils
from marble_erp.utils.langDetector import lang_detect
from marble_erp.utils.lang_translate import lang_translate

class CashLedgerSerializer(serializers.ModelSerializer):
  class Meta:
    model = CashLedger
    fields = '__all__'
    # (
    #   'ID',
    #   'ACCT_ID',
    #   'ORDINAL',
    #   # 'TRANSC_TYP',
    #   'TRANSC_DESC',
    #   'EARNING',
    #   'EXPENSE',
    #   'BALANCE',
    #   'REC_ADD_DT',
    #   'REC_ADD_BY'
    # )
    depth=1

class AddCashLedgerSerializer(serializers.ModelSerializer):

  class Meta:
    model = CashLedger
    fields = '__all__'
  def create(self, validate_data):
        TRANSC_DESC = validate_data.pop('TRANSC_DESC')
        convertFrom, convertTo = lang_detect(TRANSC_DESC)
        validate_data["TRANSC_DESC"], validate_data["TRANSC_DESC_UR"]  = lang_translate(stringToConvert=TRANSC_DESC, from_lang=convertFrom, to_lang=convertTo)
     
        created_acct = CashLedger.objects.create(**validate_data)
        return created_acct
