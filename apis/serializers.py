from django.db.models import fields
from rest_framework import serializers
from useraccount.models import AdminUser,LoginUser,BaseUser,InformativeUser,StaffUser,SupplierUser,CustomerUser,CustomerGroups
from dashboard.models import Bank, Barcode_storage,Product,Category,Brand,Units,Category,SubCategory,Purchase,Sell,Expenses,Expenses_category,Add_Payments,Purchase_info
from django.contrib.auth.models import User


class AdminSerializers(serializers.ModelSerializer):
    class Meta:
        model = AdminUser
        fields = '__all__'


class StaffSerializers(serializers.ModelSerializer):
    class Meta:
        model = StaffUser
        fields = '__all__'


class SupplierSerializers(serializers.ModelSerializer):
    class Meta:
        model = SupplierUser
        fields = '__all__'

class CustomerGroupSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomerGroups
        fields = '__all__'

class CustomerSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        fields = '__all__'

class BankSerializers(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__'


# from my side..
class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        depth = 2


class BrandSerializers(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class UnitsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Units
        fields = '__all__'


class SubCategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'


class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class PurchaseSerializers(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = '__all__'


class PayementSerializers(serializers.ModelSerializer):
    class Meta:
        model = Add_Payments
        fields = '__all__'   


class PurchaseInfoSerializers(serializers.ModelSerializer):

    class Meta:
        model = Purchase_info
        fields = '__all__'         


class SellSerializers(serializers.ModelSerializer):
    class Meta:
        model = Sell
        exclude = ['ref_no', 'order_tax', 'invoice_no']


class AddExpensesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Expenses
        # exclude = ['status', 'created_on', 'ref_no']
        fields = '__all__'


class ExpensesCategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Expenses_category
        fields = '__all__'


class ProductByBarcodeSerializer(serializers.ModelSerializer):

    product_name = serializers.SerializerMethodField()
    unit_price = serializers.SerializerMethodField()
    product_mrp = serializers.SerializerMethodField()

    class Meta:
        model = Barcode_storage
        fields = ['barcode_no', 'product_name', 'unit_price', 'product_mrp']

    def get_product_name(self, obj):
        return obj.product_name.product_name

    def get_unit_price(self, obj):
        if obj.product_name.selling_price_tax_type == 'E':
            return obj.product_name.selling_price_exc_tax
        else:
            return obj.product_name.selling_price

    def get_product_mrp(self, obj):
        return obj.product_name.prod_mrp