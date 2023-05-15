from rest_framework import serializers
# models imports
from finance.model.Currency import Currency


class CurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = (
            'CURNCY_ID',
            'ISO_CODE',
            'SIGN',
            'COUNTRY',
            'CURENCY_NAME',
            'COUNTRY_CODE_CNTRY_ABB'
        )
