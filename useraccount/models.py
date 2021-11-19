from django.db import models
from django.contrib.auth.models import User
from div_settings.models import BusinessLocation


class ContentType(models.Model):
    app_label = models.CharField(max_length=100)
    status = models.IntegerField(default=1)

    def __str__(self):
        return str(self.app_label)


class Permission(models.Model):
    permit = models.CharField(max_length=50)
    status = models.BooleanField(default=0)
    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE,null=True,blank=True,default=1)
    
    def __str__(self):
        return str(self.permit)


class Role(models.Model):
    deltypes = (
        (0, False),
        (1, True),
    )
    title = models.CharField(max_length=50)
    permissions_provided = models.ManyToManyField(Permission)
    is_deleted = models.IntegerField(default=0, choices=deltypes)

    def __str__(self):
        return str(self.title)


class BaseUser(models.Model):
    first_name = models.CharField(max_length=50,blank=True,null=True)
    last_name = models.CharField(max_length=50,blank=True,null=True)
    mobile = models.CharField(max_length=20,blank=True,null=True)
    email = models.EmailField(max_length=50,blank=True,null=True)
    date_added = models.DateTimeField(blank=True,null=True, auto_now_add=True)
    

class SalesCommisionAgent(BaseUser):
    adress = models.CharField(max_length=50)
    Sales_Commission_Percentage =models.FloatField(default=0)

    class Meta:
        db_table = 'SalesCommisionAgent'


class LoginUser(BaseUser):
    deltypes = (
        (0, False),
        (1, True),
    )

    Prefix = models.CharField(max_length=10,blank=True,null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    birth_date =  models.DateField(blank=True,null=True)
    marital_status =  models.CharField(max_length=100,blank=True) 
    blood_group = models.CharField(max_length=50)
    social_link = models.CharField(max_length=100,blank=True)
    id_proof_front = models.FileField(upload_to='docs/imge',null=True,blank=True)
    id_proof_back = models.FileField(upload_to='docs/imge',null=True,blank=True)
    contact = models.CharField(max_length=50)
    permanent_address = models.CharField(max_length=100)
    current_address = models.CharField(max_length=100)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    business_location = models.ForeignKey(BusinessLocation, on_delete=models.SET_NULL, null=True, blank=True)
    guardian_name = models.CharField(max_length=50,blank=True)
    sales_commission_percentage = models.FloatField(default=0)
    account_holder_name = models.CharField(max_length=30,blank=True)
    account_number = models.CharField(max_length=50,blank=True)
    bank_name= models.CharField(max_length=50,blank=True)
    branch = models.CharField(max_length=50,blank=True)
    tax_payer_id = models.CharField(max_length=50,blank=True)
    bank_identifier_code = models.CharField(max_length=50,blank=True)
    is_deleted = models.IntegerField(default=0, choices=deltypes)


class AdminUser(LoginUser):
    pass

    class Meta:
        db_table = 'AdminUser' 
    
    def __str__(self):
        return '{}'.format(self.username)


class StaffUser(LoginUser):
    pass
    
    class Meta:
        db_table = 'StaffUser'

    def __str__(self):
        return '{}'.format(self.username)


class InformativeUser(BaseUser):
    deltypes = (
        (0, False),
        (1, True),
    )
    status_choices = [("S", 'suppliers'),('C','customers'),('B','both')]
    
    business_name = models.CharField(max_length=30,blank=True,null=True)
    contact_id = models.CharField(max_length=50,blank=True,null=True)
    tax_number = models.CharField(max_length=50,null=True,blank=True)
    opening_balance = models.FloatField(default=0,blank=True,null=True)
    pay_term = models.CharField(max_length=50)
    business_location = models.ForeignKey(BusinessLocation, on_delete=models.SET_NULL, null=True)
    alternative_contact = models.CharField(max_length=60,null=True,blank=True)
    Landline = models.CharField(max_length=50,null=True,blank=True)
    city = models.CharField(max_length=60,null=True,blank=True)
    state = models.CharField(max_length=60,null=True,blank=True)
    country = models.CharField(max_length=60,null=True,blank=True)
    land_mark = models.CharField(max_length=60,null=True,blank=True)
    Contact_type = models.CharField(max_length=1,choices=status_choices)
    address = models.CharField(max_length=50,blank=True,null=True)
    is_deleted = models.IntegerField(default=0, choices=deltypes)
    
    # custom_field1 = models.CharField(max_length=40,null=True,blank=True)
    # custom_field2 = models.CharField(max_length=40,null=True,blank=True)
    # custom_field3 = models.CharField(max_length=40,null=True,blank=True)
    # custom_field4 = models.CharField(max_length=40,null=True,blank=True)


class SupplierUser(InformativeUser):

    total_purchase_due = models.FloatField(default=0, null=True, blank=True)
    total_purchase_return_due = models.FloatField(default=0, null=True, blank=True)

    class Meta:
        db_table = 'SupplierUser'


class CustomerGroups(models.Model):

    deltypes = (
        (0, False),
        (1, True),
    )
    name = models.CharField(max_length=50)
    percentage = models.FloatField(blank=True,null=True)
    is_deleted = models.IntegerField(default=0, choices=deltypes)

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        db_table = 'customergroup'


class CustomerUser(InformativeUser):

    customer_group = models.ForeignKey(CustomerGroups, on_delete=models.SET_NULL, null=True)
    total_sales_due = models.FloatField(default=0, null=True, blank=True)
    total_sales_return_due = models.FloatField(default=0, null=True, blank=True)
    credit_limit = models.FloatField(default=0,blank=True,null=True)

    class Meta:
        db_table = 'CustomerUser'
    
    def __str__(self):
        return '{}'.format(self.first_name)