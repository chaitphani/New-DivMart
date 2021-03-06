from django.contrib import admin
from dashboard.models import *
from sale.models import *
from useraccount.models import *
from membership.models import *
from div_settings.models import *


class Add_PaymentAdmin(admin.ModelAdmin):
    list_display = ('amount', 'payment_account',)

class SellAdmin(admin.ModelAdmin):
    list_display = ('ref_no', 'customer', 'total_payable', 'status')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'category', 'unit' , 'brand', 'current_stock', 'status')
    list_filter = ('status', 'selling_price_tax_type', 'product_type', )
    search_fields = ('product_name',)
    
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'purchase_quantity', 'sub_total',)
    list_filter = ('product_name__business_location__name', 'product_name__status',)

class ItemSoldAdmin(admin.ModelAdmin):
    list_display = ('items_name', 'quantity', 'sub_total')

class SupplierUserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'email', 'business_name', 'city', 'total_purchase_due')
 
class CustomerUserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'email', 'total_sales_due')

class RoleAdmin(admin.ModelAdmin):
    list_display = ('title',)

class ContentTypeAdmin(admin.ModelAdmin):
    list_display = ('app_label', 'status')

class PermissionAdmin(admin.ModelAdmin):
    list_display = ('permit', 'content_type')


admin.site.register(BusinessLocation)
admin.site.register(TaxRate)

admin.site.register(Bank)
admin.site.register(SubCategory)
admin.site.register(Brand)
admin.site.register(Units)
admin.site.register(Product, ProductAdmin)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Purchase_info)
admin.site.register(Category) 
admin.site.register(Barcode_storage) 
admin.site.register(StockTransfer) 
admin.site.register(StockAdjustment) 
admin.site.register(SellingPriceGroup) 
admin.site.register(ProductVariation) 
admin.site.register(Stock) 
admin.site.register(Expenses_category) 
admin.site.register(Expenses) 
admin.site.register(PaymentAccount)
admin.site.register(Add_Payments, Add_PaymentAdmin) 
admin.site.register(Sell, SellAdmin) 
admin.site.register(ItemSold, ItemSoldAdmin) 
admin.site.register(StockProdTransfer) 
admin.site.register(StockProdAdjustment) 

admin.site.register(ContentType, ContentTypeAdmin)
admin.site.register(AdminUser)
admin.site.register(StaffUser)
admin.site.register(Permission, PermissionAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(CustomerUser, CustomerUserAdmin)
admin.site.register(CustomerGroups)
admin.site.register(SupplierUser, SupplierUserAdmin) 


class RegisteredMembersAdmin(admin.ModelAdmin):
    list_display = ('fname', 'self_ref_id', 'sponser_id', 'commission', 'status', 'member_amount')
    list_filter = ('status',)

class WithdrawlTransactionRequestsAdmin(admin.ModelAdmin):
    list_display = ('member', 'amount', 'payment_status', 'created')
    list_filter = ('payment_status', )
    date_hierarchy = 'created'
    

admin.site.register(RegisteredMembers, RegisteredMembersAdmin)
admin.site.register(PointsTransactionRequests)
admin.site.register(WithdrawlTransactionRequests, WithdrawlTransactionRequestsAdmin)
admin.site.register(CreditedPoints)
