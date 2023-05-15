from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from accounts.model.Account import Accounts,account_type
#  Custom User Manager


class acct_type_id(models.Model):

    class Meta:
        verbose_name = _("acct_type_id")
        verbose_name_plural = _("acct_type_id")

    ACCT_ID_TYPE_LINK = models.AutoField(
        primary_key=True,
        null=False,
        blank=False
    )
    
    ACCT_ID = models.ForeignKey(
        Accounts,
        on_delete=models.CASCADE, 
        db_column="ACCT_ID",
         null=False
    )
    ACCT_TYP_ID =models.ForeignKey(
        account_type,
        on_delete=models.CASCADE, 
        db_column="ACCT_TYP_ID",
         null=False
    )

    IS_ACTIVE = models.IntegerField(
        null=False,
        default=1
    )

    REC_ADD_DT = models.DateTimeField(
        auto_now_add=True
    
    )
    REC_MOD_DT = models.DateTimeField(
        auto_now_add=True
    )

    REC_ADD_BY = models.IntegerField(
        blank=False,
        null=False,
        default=0
    )

    REC_MOD_BY = models.IntegerField(
        blank=False,
        null=False,
        default=0
    )

    class Meta:

        db_table = 'acct_type_id'

