from django.contrib.auth.models import User
from useraccount.models import *
from div_settings.models import BusinessLocation, TaxRate


class Bank(models.Model):

    user = models.OneToOneField(User,on_delete=models.SET_NULL, null="true")
    account_holder_name = models.CharField(max_length=30)
    account_number = models.CharField(max_length=50)
    bank_name= models.CharField(max_length=50)
    branch = models.CharField(max_length=50)
    tax_payer_id = models.CharField(max_length=50)
    branch = models.CharField(max_length=50)
    bank_identifier_code = models.CharField(max_length=50)

    class Meta:
        db_table = 'Bank'


class SubCategory(models.Model):
    name = models.CharField(max_length=50)
    status = models.BooleanField(default=True)

    
    def __str__(self):
        return str(self.name)


class Category(models.Model):

    name = models.CharField(max_length=50)
    category_code = models.CharField(max_length=15)
    sub_category = models.ManyToManyField(SubCategory)
    discription = models.TextField(null=True,blank=True)
    status = models.BooleanField(default=True)
    
    def __str__(self):
        return str(self.name)


class Brand(models.Model):

    deltypes = (
        (0, False),
        (1, True),
    )
    brand_name = models.CharField(max_length=50)
    discription = models.CharField(max_length=50, null=True,blank=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return str(self.brand_name)


class Units(models.Model):

    dec = [('Y','Yes'),('N','No')]
    deltypes = (
        (0, False),
        (1, True),
    )
    name = models.CharField(max_length=50)
    short_name = models.CharField(max_length=25)
    allow_decimal = models.CharField(max_length=1,choices=dec)
    status = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)


class PaymentAccount(models.Model):

    name = models.CharField(max_length=120)
    account_number = models.IntegerField()
    openning_balance = models.FloatField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=True)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)


class Product(models.Model):

    tax_choices = [('E','Exclusive'),('I','Inclusive')]
    prod_type = [('S','Single'),('V','Variable')]

    product_name = models.CharField(max_length=50)
    business_location = models.ForeignKey(BusinessLocation, on_delete=models.SET_NULL, null=True)

    brand = models.ForeignKey(Brand,on_delete=models.SET_NULL, null=True, blank=True)
    unit = models.ForeignKey(Units,on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True, related_name='pro_category', blank=True)
    sub_category = models.ForeignKey(SubCategory,on_delete=models.SET_NULL, null=True, blank=True)
    SKU = models.CharField(max_length=50)
    barcode_type = models.CharField(max_length=50, null=True, blank=True)
    alert_quantity = models.CharField(max_length=30,null=True, blank=True)
    Product_description = models.CharField(max_length=500, null=True, blank=True)
    product_image = models.ImageField(upload_to='media/image/products',null=True, blank=True,default=None)
    weight = models.FloatField(default=0, null=True, blank=True)
    applicable_tax = models.ForeignKey(TaxRate, on_delete=models.SET_NULL, null=True, blank=True)
    product_type = models.CharField(max_length=1, choices=prod_type, null=True, blank=True)
    prod_mrp = models.FloatField(max_length=120, null=True, blank=True)
    sale_mrp = models.FloatField(default=0)
    selling_price_tax_type = models.CharField(max_length=1, choices=tax_choices, null=True, blank=True)
    selling_price = models.FloatField(default=0, null=True, blank=True)
    selling_price_exc_tax =  models.FloatField(default=0, null=True)
    purchase_price = models.FloatField(default=0, null=True, blank=True)
    purchase_price_exc_tax =  models.FloatField(default=0, null=True, blank=True)
    purchase_price_inc_tax =  models.FloatField(default=0, null=True, blank=True)
    margin =  models.FloatField(default=0, null=True, blank=True)
    current_stock = models.FloatField(default=0, null=True, blank=True)
    status = models.BooleanField(default=True)

    # custom_field1 = models.CharField(max_length=50,null=True,blank=True)
    # custom_field2 = models.CharField(max_length=50,null=True,blank=True)
    # custom_field3 = models.CharField(max_length=50,null=True,blank=True)
    # custom_field4 = models.CharField(max_length=50,null=True,blank=True)

    def __str__(self):
        return str(self.product_name)


class Add_Payments(models.Model):

    pay_choice = ((0, "cash"), (1, "card"), (2, "cheque"), (3, "Bank transfer"), (4, "other"),)

    amount = models.FloatField()
    payment_method = models.IntegerField(default=1, choices=pay_choice)
    payment_account = models.ForeignKey(PaymentAccount, on_delete=models.SET_NULL, null=True)
    payment_notes = models.CharField(max_length=100, null=True, blank=True)
    payment_due = models.FloatField(null=True, blank=True)
    payment_status = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    

class Purchase_info(models.Model):

    # deltypes = ((0, False),(1, True),)
    per_choice = ((0, False),(1, True),)

    supplier = models.ForeignKey(SupplierUser,on_delete=models.SET_NULL, null=True)
    ref_no = models.CharField(max_length=40)
    purchase_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    # purchase_status = models.CharField(max_length=50)
    business_location = models.ForeignKey(BusinessLocation, on_delete=models.SET_NULL, null=True)
    documents = models.FileField(upload_to="purchase/docs", blank=True,null=True)
    grand_total = models.FloatField(default=0,null=True)
    discount_type = models.CharField(max_length=15,blank=True)
    Discount_amount = models.FloatField(default=0)
    discount = models.CharField(max_length=100,blank=True)
    purchase_tax = models.CharField(max_length=100,blank=True)
    purchase_tax_amount = models.FloatField(default=0)
    shipping_details = models.CharField(max_length=100)
    additional_ship_charges = models.FloatField(default=0)
    purchase_total = models.FloatField(default=0)
    Additional_notes = models.TextField()
    payment_info = models.ForeignKey(Add_Payments,on_delete=models.SET_NULL, null=True)
    purchase_return = models.IntegerField(default=0,choices=per_choice)
    status = models.BooleanField(default=True)

    def __str__(self):
        return str(self.supplier.first_name)


class Purchase(models.Model):

    deltypes = ((0, False),(1, True),)
    per_choice = ((0, False),(1, True),)

    product_name= models.ForeignKey(Product,on_delete=models.SET_NULL, null=True)
    purchase_details = models.ForeignKey(Purchase_info,on_delete=models.SET_NULL, null=True)
    purchase_quantity = models.BigIntegerField(default=0)
    unit_cost_before_discount = models.FloatField(default=0)
    unit_cost_before_tax = models.FloatField(default=0)
    discount_percentage = models.FloatField(default=0)
    sub_total =  models.FloatField(default=0)
    product_tax = models.FloatField(default=0)
    net_costs = models.FloatField(default=0)
    line_total = models.FloatField(default=0,null=True)
    profit_margin = models.FloatField(default=0)
    unit_selling_price = models.FloatField(default=0)
    status = models.BooleanField(default=True)
    purchase_return = models.IntegerField(default=0,choices=per_choice)

    def __str__(self):
        return '{}-{}'.format(self.product_name, self.net_costs)


class Sell(models.Model):

    dis_choice = (("F","Fixed"),("P","Percentage"))
    st_choice = (("Final","Final"),("Draft","Draft"),("Quotation","Quotation"), ("Credit", "Credit"))
    per_choice = ((0, False),(1, True),)

    ref_no = models.CharField(max_length=40)
    business_location = models.ForeignKey(BusinessLocation, on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(CustomerUser, on_delete=models.SET_NULL, null=True)
    pay_term = models.CharField(max_length=80, null=True, blank=True)
    sale_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=1, choices=st_choice, default='F')
    total_amount = models.FloatField()
    discount_type = models.CharField(max_length=1, choices=dis_choice, null=True, blank=True)
    discount_amount = models.FloatField(default=0.0)
    shipping_details = models.CharField(max_length=100, null=True, blank=True)
    shipping_charges = models.FloatField(default=0.0)
    total_payable = models.FloatField()
    sell_notes = models.TextField(null=True, blank=True)
    payment_info = models.ForeignKey(Add_Payments, on_delete=models.SET_NULL, null=True)
    invoice_no = models.IntegerField()
    order_tax = models.FloatField(null=True, blank=True)
    sale_return = models.IntegerField(default=0, choices=per_choice)
    cashier = models.ForeignKey(StaffUser, on_delete=models.SET_NULL, null=True)
    is_deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return '{}-{}'.format(self.customer.first_name, self.total_payable)


class Barcode_storage(models.Model):

    product_name = models.ForeignKey(Product,on_delete=models.DO_NOTHING)
    barcode_type = models.CharField(max_length=50)
    barcode_no = models.CharField(max_length=200)

    def __str__(self):
        return str(self.product_name)


class Expenses_category(models.Model):

    name = models.CharField(max_length=50)
    category_code = models.CharField(max_length=50)
    status = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)


class Expenses(models.Model):

    status_choice = (('Paid' ,'Paid'), ('Unpaid', 'Unpaid'), ('Rejected', 'Rejected'))

    ref_no = models.CharField(max_length=50, blank=True)
    expense_category = models.ForeignKey(Expenses_category,on_delete=models.CASCADE)
    business_location = models.ForeignKey(BusinessLocation, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField()
    payment_status = models.CharField(max_length=50, choices=status_choice, default='Unpaid')
    amount = models.FloatField(default=0)
    expense_note = models.CharField(max_length=100, blank=True) 
    docs = models.ImageField(upload_to='media/expenses/image', null=True, blank=True)
    status = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.amount)


class StockTransfer(models.Model):

    date = models.DateTimeField(auto_now_add=True)
    ref_no = models.CharField(max_length=120)
    location_from = models.ForeignKey(BusinessLocation, on_delete=models.SET_NULL, null=True, related_name='location_from_business')
    location_to = models.ForeignKey(BusinessLocation, on_delete=models.SET_NULL, null=True, related_name='location_to_business')
    total_amount = models.CharField(max_length=120)
    shipping_charges = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=True)
    
    def __str__(self):
        return '{}--{}'.format(self.location_from.name, self.location_to.name)


class StockProdTransfer(models.Model):
    
    stock_transfer = models.ForeignKey(StockTransfer, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.CharField(max_length=120)
    unit_price = models.CharField(max_length=120)
    sub_total = models.CharField(max_length=120)
    date = models.DateTimeField(auto_now_add=True)

    def __str___(self):
        return '{}-{}'.format(self.stock_transfer.location_from.name, self.product.product_name)


class StockAdjustment(models.Model):

    adjst_choices = (('1', 'Normal'), ('2', 'Abnormal'),)

    business_location = models.ForeignKey(BusinessLocation, on_delete=models.SET_NULL, null=True)
    ref_no = models.CharField(max_length=120)
    adjustment_type = models.CharField(max_length=1, choices=adjst_choices)
    total_amount_recovered = models.CharField(max_length=120)
    reason = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=True)
    date_of_adjust = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return '{}-{}'.format(self.ref_no, self.business_location.name)


class StockProdAdjustment(models.Model):

    stock_adjustment = models.ForeignKey(StockAdjustment, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.CharField(max_length=120)
    unit_price = models.CharField(max_length=120)
    sub_total = models.CharField(max_length=120)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}-{}'.format(self.stock_adjustment.ref_no, self.product.product_name)


class SellingPriceGroup(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)


class ProductVariation(models.Model):

    variation_name = models.CharField(max_length=120)
    variation_values = models.CharField(max_length=120)

    def __str__(self):
        return str(self.variation_name)


class Stock(models.Model):
    
    sku = models.IntegerField(default=0)
    location = models.CharField(max_length=120)
    quantity = models.FloatField()
    unit_cost = models.FloatField()
    lot_number = models.IntegerField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)