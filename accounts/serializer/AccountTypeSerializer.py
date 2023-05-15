from rest_framework import serializers
from accounts.model.Account import Accounts

class AccountTypeSerializer(serializers.ModelSerializer):

  class Meta:
    model = Accounts
    fields=  (
      'ACCT_AUTH_ID',
      'ACCT_ID',
      'ACCT_TYPE_ID'
    )
