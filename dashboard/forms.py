from django import forms
from .models import *
from useraccount.models import Role


# from my side...
# class StockTransferForm(forms.ModelForm):
#     class Meta:
#         model = StockTransfer
#         fields = '__all__'
#         exclude = ['ref_no']


class StockAdjustmentForm(forms.ModelForm):
    class Meta:
        model = StockAdjustment
        fields = '__all__'
        exclude = ['ref_no']


class BrnadForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = '__all__'
        exclude = ['status']


class UnitsForm(forms.ModelForm):
    class Meta:
        model = Units
        fields = '__all__'
        exclude = ['status']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'category_code', 'sub_category', 'discription']


class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = '__all__'
        exclude = ['status']

    
class SellingPriceGroupForm(forms.ModelForm):
    class Meta:
        model = SellingPriceGroup
        fields = '__all__'
        exclude = ['status']


class VariationForm(forms.ModelForm):
    class Meta:
        model = ProductVariation
        fields = '__all__'


class PaymentAccountForm(forms.ModelForm):
    class Meta:
        model = PaymentAccount
        fields = '__all__'
        exclude = ['status', 'added_on']


class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = '__all__'
        exclude = ['status']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['status', 'barcode_type']

    # def validate_applicable_tax()