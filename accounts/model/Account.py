from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
#  Custom User Manager


class UserManager(BaseUserManager):

    def create_user(self, email, FIRST_NAME, FIRST_NAME_UR,LAST_NAME,LAST_NAME_UR, password=None, confirm_password=None , REC_MOD_BY =0, REC_ADD_BY=0):
        """
        Creates and saves a User with the given email, name, tc and password.
        """
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            FIRST_NAME=FIRST_NAME,
            LAST_NAME=LAST_NAME,
            FIRST_NAME_UR=FIRST_NAME_UR,
            LAST_NAME_UR=LAST_NAME_UR,
            REC_ADD_BY=REC_ADD_BY,
            REC_MOD_BY=REC_MOD_BY,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, FIRST_NAME, LAST_NAME, password=None):
        """
        Creates and saves a superuser with the given email, name, tc and password.
        """
        user = self.create_user(
            email,
            password=password,
            FIRST_NAME=FIRST_NAME,
            LAST_NAME=LAST_NAME,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


#  Custom User Model
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )

    FIRST_NAME = models.CharField(max_length=100 , blank=True)

    FIRST_NAME_UR = models.CharField(
        max_length=45,
        null=True
    )

    LAST_NAME_UR = models.CharField(
        max_length=45,
        null=True
    )

    LAST_NAME = models.CharField(max_length=100 , blank=True)

    is_active = models.BooleanField(default=True)

    is_admin = models.BooleanField(default=False)

    REC_ADD_DT = models.DateTimeField(
        auto_now_add=True
    )

    REC_ADD_BY = models.IntegerField(
        blank=False,
        null=False,
        default=0
    )

    REC_MOD_DT = models.DateTimeField(
        auto_now=True
    )

    REC_MOD_BY = models.IntegerField(
        blank=False,
        null=False,
        default=0
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['FIRST_NAME', 'LAST_NAME']

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    @property
    def addresses(self):
        return Address.objects.filter(USER=self.id)
    @property
    def address_info(self):
        return Address.objects.filter(USER=self.id)

    @property
    def contact_info(self):
        return Phone_Numbers.objects.filter(USER=self.id)

    @property
    def account(self):
        return Accounts.objects.get(USER_ID=self.id)

    @property
    def roles(self):
        pass

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    class Meta:

        db_table = 'users'


# Address Models
class Address(models.Model):

    ADDR_ID = models.AutoField(
        primary_key=True,
        null=False,
        blank=False
    )

    USER = models.ForeignKey(
        User,
        related_name="fk_addrs_user",
        on_delete=models.CASCADE, db_column="USER",
        null=True
    )

    IS_PRIMARY = models.IntegerField(
        default=0
    )

    ADDRESS = models.CharField(
        max_length=500,
        null=True
    )

    ADDRESS_UR = models.CharField(
        max_length=500,
        null=True
    )

    TEHSIL = models.CharField(
        max_length=45,
        null=True
    )

    TEHSIL_UR = models.CharField(
        max_length=45,
        null=True
    )

    PROVINCE = models.CharField(
        max_length=45,
        null=True
    )
    
    PROVINCE_UR = models.CharField(
        max_length=45,
        null=True
    )

    POSTAL_CODE = models.CharField(
        max_length=10,
        null=True
    )

    POSTAL_CODE_UR = models.CharField(
        max_length=10,
        null=True
    )
    CNTRY_NM = models.CharField(
        max_length=100,
        null=True
    )

    CNTRY_NM_UR = models.CharField(
        max_length=100,
        null=True
    )

    DNM = models.IntegerField(
        default=0
    )

    CNTRY_ABB = models.CharField(
        max_length=45,
        null=True
    )

    class Meta:

        db_table = 'address'


# Phone Number Model
class Phone_Numbers(models.Model):

    PH_ID = models.AutoField(
        primary_key=True,
        null=False,
        blank=False
    )

    USER = models.ForeignKey(
        User,
        related_name="fk_ph_user",
        on_delete=models.CASCADE, db_column="USER",
        null=True
    )

    IS_PRIMARY = models.IntegerField(
        default=0
    )

    PH_NUM = models.CharField(
        max_length=45,
        blank=True,
        null=True,
    )

    IS_CELL = models.IntegerField(
        null=True,
        blank=True,
        default=1
    )

    class Meta:

        db_table = 'phone_numbers'



# AccountType Model
class account_type(models.Model):

    ACCT_TYPE_ID = models.AutoField(
        primary_key=True,
        null=False,
        blank=False
    )

    ACCT_TYPE_NM = models.CharField(
        max_length=45,
        null = False
    )
    ACCT_TYPE_NM_UR = models.CharField(
        max_length=45,
        null = True
    )

    REC_ADD_DT = models.DateTimeField(
        auto_now_add=True
    )

    REC_ADD_BY = models.IntegerField(
        blank=False,
        null=False,
        default=0
    )

    
    class Meta:

        db_table = 'account_type'


# Accounts Model
class Accounts(models.Model):

    ACCT_ID = models.AutoField(
        primary_key=True,
        null=False,
        blank=False
    )

    ACCT_TITLE = models.CharField(
        max_length=45,
    )

    ACCT_TITLE_UR = models.CharField(
        max_length=45,
        null=True
    )


    ACCT_REF = models.CharField(
        max_length=45,
    )

    acct_type = models.ManyToManyField(
        account_type,
        verbose_name=_("acct_type"),
        blank=True,
        help_text=_(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
        related_name="accounts_set",
        related_query_name="accounts",
    )

    
    ACCT_REF_UR = models.CharField(
        max_length=45,
        null=True
    )
    

    ACCT_DESC = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    ACCT_DESC_UR = models.CharField(
       max_length=45,
        null=True
    )


    ACCT_TYP = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    USER_ID = models.ForeignKey(
        User,
        on_delete=models.CASCADE, 
        db_column="USER_ID",
         null=True
    )
    IS_ACTIVE = models.IntegerField(
        null=False,
        default=1
    )

    OPNG_BLNCE = models.IntegerField(
        default=0
    )

    CLOSNG_BLNCE = models.IntegerField(
        default=0
    )

    ACCT_CREATE_DT = models.DateTimeField(
        auto_now_add=False
    )

    REC_ADD_DT = models.DateTimeField(
        auto_now_add=True
    )

    REC_ADD_BY = models.IntegerField(
        blank=False,
        null=False,
        default=0
    )

    REC_MOD_DT = models.DateTimeField(
        auto_now=True
    )

    REC_MOD_BY = models.IntegerField(
        blank=False,
        null=False,
        default=0
    )
    
    @property
    def ACCOUNT_USER(self):
        return self.USER_ID

    @property
    def address_info(self):
        return Address.objects.filter(USER=self.USER_ID)

    @property
    def contact_info(self):
        return Phone_Numbers.objects.filter(USER=self.USER_ID)
    
    @property
    def ACCT_TYPE_ID(self):
        pass

    class Meta:

        db_table = 'accounts'



    
class acct_id_type_id_link(models.Model):

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
    ACCT_TYPE_ID =models.ForeignKey(
        account_type,
        on_delete=models.CASCADE, 
        db_column="ACCT_TYPE_ID",
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

        db_table = 'acct_id_type_id_link'



