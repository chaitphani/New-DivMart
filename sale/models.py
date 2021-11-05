from django.db import models
from div_settings.models import BusinessLocation
from useraccount.models import StaffUser
from dashboard.models import *


class Sales(models.Model):
    
    customer_name = models.CharField(max_length=50)
    contact = models.CharField(max_length=60)
    no_of_item = models.FloatField(default=0,max_length=50)
    grand_total = models.FloatField(default=0,max_length=50)
    total_tax = models.FloatField(default=0,max_length=50)
    total_discount = models.FloatField(default=0,max_length=50)
    bill_no = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True,editable=False)
    voucher_no = models.CharField(max_length=50)
    business_location = models.ForeignKey(BusinessLocation, on_delete=models.SET_NULL, null=True)
    types_of_payment = models.CharField(max_length=50,null=True,blank=True)
    # payment_id
    total_quantity = models.FloatField(default=0,null=True,blank=True)
    total_quantity = models.FloatField(default=0,null=True,blank=True)
    cashier = models.ForeignKey(StaffUser,on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = 'Sales'


class ItemSold(models.Model):

    sell = models.ForeignKey(Sell, on_delete=models.SET_NULL, null=True)
    items_name = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    # sale_mrp = models.FloatField(default=0)
    price = models.FloatField(default=0)
    quantity = models.FloatField(default=50)
    sub_total = models.FloatField(default=0)
    date =models.DateTimeField(auto_now_add=True,editable=True)

    # discount = models.FloatField(default=0)
    # tax = models.FloatField(default=0)
    # brand_id  

    # def __str__(self):
    #     return '{}-{}'.format(self.sell.customer, self.items_name.product_name)