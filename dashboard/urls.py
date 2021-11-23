from os import name
from django.urls import path
from dashboard import views
from sale import views as sale_views
from div_settings import views as business_views


urlpatterns = (

    # path('admin_dashboard',views.admin_dashboard,name='admin_dashboard'),
    # path('cashier_dashboard',views.cashier_dashboard,name='cashier_dashboard'),

    # path('admin_manage_users',views.admin_manage_users,name='manage_users'),
    # path('user_edit/<int:id>/edit',views.user_edit,name='user_edit'),
    # path('view_user/<int:id>',views.user_details,name='view_user'),
    # path('delete_user/<int:id>',views.delete_user,name='delete_user'),
    # path('admin_user_creation',views.admin_user_creation,name="admin_user_creation"),

    path('',views.home, name='home'),
    path('user',views.user, name='user'),

    path('admin_user_creation',views.admin_user_creation, name='admin_user_creation'),
    path('user_edit/<id>',views.user_edit,name='user_edit'),
    path('user_delete/<id>',views.user_delete,name='user_delete'),
    path('sales_commission_agent',views.sales_commission_agent,name='sales_commission_agent'),
    path('supplier_detail/<int:id>',views.supplier_detail,name='supplier_detail'),
    path('supplier_delete/<id>',views.supplier_delete,name='supplier_delete'),
    
    # path('roles',views.roles, name='roles'),
    # path('role_deletion/<id>',views.role_deletion, name='role_deletion'),
    # path('add_role',views.add_role, name='add_role'),
    
    path('add_new_product',views.add_new_product, name='add_new_product'),
    path('list_purchase_return',views.list_purchase_return,name='list_purchase_return'),
    path('list_purchase',views.list_purchase,name='list_purchase'),
    path('add_purchase_return',views.add_purchase_return,name='add_purchase_return'),
    
    path('product_informtion_api/<str:product>',views.product_informtion_api,name='product_informtion_api'),
    path('list_supplier',views.list_supplier,name='list_supplier'),
    path('customer_list',views.customer_list,name='customer_list'),
    path('customer_group_detail',views.customer_group_detail,name='customer_group_detail'),
    path('delete_customer_group/<int:id>',views.delete_customer_group,name='delete_customer_group'),
    path('import_contact',views.import_contact,name='import_contact'),
    path('payment_account_book',views.payment_account_book,name='payment_account_book'),
    path('payment_balance_sheet',views.payment_balance_sheet,name='payment_balance_sheet'),
    # path('edit_role/<id>',views.edit_role,name='edit_role'),
    path('supplier_edit/<id>',views.supplier_edit,name='supplier_edit'), 

    path('list_sell_return',views.list_sell_return,name='list_sell_return'),
    path('list_discount',views.list_discount,name='list_discount'), 
    path('list_subscription',views.list_subscription,name='list_subscription'), 
    path('payment_trial_balance',views.payment_trial_balance,name='payment_trial_balance'), 
    path('payment_cash_flow',views.payment_cash_flow,name='payment_cash_flow'),
    path('payment_account_report',views.payment_account_report,name='payment_account_report'),

    # changes by basha...
    path('roles',views.roles, name='roles'),
    path('role/add',views.RoleView.as_view(), name='add_role'),
    path('role/<int:id>/update',views.RoleUpdateView.as_view(),name='edit_role'),
    path('role/<int:id>/delete',views.role_deletion, name='role_deletion'),

    path('member/direct',views.direct_members,name='direct_members'),
    path('member/manage-transactions',views.manage_transaction,name='member_direct_transaction'),
    path('member/points-transaction',views.all_point_transaction,name='all_point_transaction'),

    # changes done by.....
    path('business-locations', business_views.business_location_list, name='business-location'),
    path('business-location/<int:id>/update', business_views.business_location_update, name='business-location-update'),
    path('business-location/<int:id>/delete', business_views.business_location_delete, name='business-location-delete'),

    path('product/search',views.search_product_list, name='search_product_list'),
    path('product/search/<int:id>',views.search_product_with_id, name='search_product_with_id'),

    path('stock-transfers',views.stock_transfer_list,name='stock_transfer_list'),
    path('stock-transfer/add',views.add_stock_transfer,name='add_stock_transfer'),
    path('stock-transfer/<int:id>/update',views.edit_stock_trasfer,name='edit-stock-trasfer'),
    path('stock-transfer/<int:id>/delete',views.delete_stock_transfer,name='delete-stock-trasfer'),
    path('stock-transfer-report',views.stock_transfer_report,name='stock_transfer_report'),

    path('stock-adjustments',views.list_stock_adjustment,name='list_stock_adjustment'),
    path('stock-adjustment/add',views.add_stock_adjustment,name='add_stock_adjustment'), 
    path('stock-adjustment/<int:id>/update',views.edit_stock_adjustment,name='edit-stock-adjustment'),
    path('stock-adjustment/<int:id>/delete',views.delete_stock_adjustment,name='delete-stock-adjustment'),

    path('brands',views.brand,name='brand'),
    path('brand/<int:id>/update', views.edit_brand, name="edit-brand"),
    path('brand/<int:id>/delete', views.remove_brand, name="remove-brand"),

    path('units',views.product_units,name='units-list'),
    path('unit/<int:id>/update',views.edit_units,name="edit-units"),
    path('unit/<int:id>/delete',views.unit_delete,name="unit-delete"),

    path('categories',views.categories,name='categories'),
    path('category/<int:id>/update',views.edit_category,name="edit-category"),
    path('category/<int:id>/delete',views.delete_category,name="delete-category"),

    path('sub-categories',views.sub_category,name='sub-category'),
    path('sub-category/<int:id>/update',views.edit_sub_ctaegory,name="edit-sub-category"),
    path('sub-category/<int:id>/delete',views.delete_sub_category,name="delete-sub-category"),

    path('products',views.list_products, name='list_products'),
    path('product/<int:id>/update',views.edit_new_product, name='edit_new_product'),
    path('product/<int:id>/remove',views.product_delete, name='product_delete'),


    path('print-label',views.print_label, name='print_label'),

    path('selling-price-groups',views.add_sellingprice_group,name='selling-price-groups'),
    path('selling-price-group/<int:id>/update',views.edit_sellingprice_group,name="edit-selling-price-groups"),
    path('selling-price-group/<int:id>/delete',views.delete_sellingprice_group,name="delete-selling-price-groups"),

    path('variations',views.variations,name='variations'),
    path('variation/<int:id>/update',views.edit_variations,name="edit-variation"),
    path('variation/<int:id>/delete',views.delete_variation,name="delete-variation"),

    path('expenses-category',views.add_expenses_category,name='add_expenses_category'),  
    path('expenses-category/<id>/delete',views.delete_exp_category,name='delete_exp_category'), 

    path('expenses',views.list_expenses,name='list_expenses'),
    path('expenses/add',views.add_expenses,name='add_expenses'),

    path('product/import',views.import_products, name='import_product'),
    path('opening-stock/import',views.import_opening_stock,name='import_opening_stock'),

    path('sales', sale_views.sale_list,name='sale_list'),
    path('sale/add', sale_views.sale_add,name='sale_add'),
    path('sale/<int:id>/edit', sale_views.edit_sales,name='sale_edit'),
    path('sale/<int:id>/delete', sale_views.delete_sale,name='delete_sale'),

    path('pos',views.list_pos,name='list_pos') ,
    path('pos/add',views.dashboard_pos,name='dashboard_pos'),

    path('payment-accounts', views.payment_account, name='payment_accounts'),
    path('payment-account/<int:id>/update', views.payment_account_edit, name='payment_account_edit'),
    path('payment-account/<int:id>/delete', views.payment_account_remove, name='payment_account_remove'),

    path('drafts',views.list_draft,name='list_draft'),
    path('quotations',views.list_quotations,name='list_quotations'),

    path('purchases',views.list_purchase,name='list_purchase'),
    path('purchase/add',views.add_purchase,name='add_purchase'),
    path('purchase/<id>/update',views.edit_purchase,name='edit_purchase'), 
    path('purchase/<int:id>/view',views.view_purchase,name='view_purchase'), 

	path('members',views.new_members,name='new_members'),
    path('member/<int:id>/update',views.edit_members,name='edit_members'),
    path('member/<int:id>/view',views.view_members,name='view_members'),
    path('member/manage',views.members,name='members'),
    path('member/<int:id>/delete', views.member_status_change, name='member-remove'),

    path('member/withdraw-requests',views.all_withdrawal_request,name='all_withdrawal_request'),

    path('invoice', views.barcode_data),

    path('tax-rate', business_views.add_tax_rate, name='tax-rate'),
    path('tax-rate/<int:id>/update', business_views.edit_tax_rate, name='tax-rate-update'),
    path('tax-rate/<int:id>/delete', business_views.delete_tax_rate, name='tax-rate-remove'),

    # reports part urls start here
    path('payment_account_report',views.payment_account_report,name='payment_account_report'),
    path('purchase_sales_report',views.purchase_sales_report,name='purchase_sales_report'),
    path('profit_loss_report',views.profit_loss_report,name='profit_loss_report'),
    path('tax_report',views.tax_report,name='tax_report'),
    path('customer_supplier_report',views.customer_supplier_report,name='customer_supplier_report'),
    path('customer_groups_report',views.customer_groups_report,name='customer_groups_report'),
    path('stock_report',views.stock_report,name='stock_report'),
    path('lot_report',views.lot_report,name='lot_report'),
    path('trending_products_report',views.trending_products_report,name='trending_products_report'),
    path('stock_adjustment_report',views.stock_adjustment_report,name='stock_adjustment_report'),
    path('items_report',views.items_report,name='items_report'),
    path('product_purchase_report',views.product_purchase_report,name='product_purchase_report'),
    path('product_sell_report',views.product_sell_report,name='product_sell_report'),
    path('purchase_payment_report',views.purchase_payment_report,name='purchase_payment_report'),
    path('sell_payment_report',views.sell_payment_report,name='sell_payment_report'),
    path('expense_report',views.expense_report,name='expense_report'),
    path('register_report',views.register_report,name='register_report'),
    path('sales_representative_report',views.sales_representative_report,name='sales_representative_report'),
    path('transaction_history',views.transaction_history,name='transaction_history'),
    # report API's
    path('stocks', views.StockReportView.as_view(), name='stocks'),
    path('items', views.ItemReportView.as_view(), name='items'),
    path('register-details', views.register_details, name='register_details'),

    path('invoice/<int:id>/view', views.invoice_view, name='invoice_view'),

    path('customer/<int:id>/view',views.customer_detail,name="customer_detail"),
    path('customer/<int:id>/edit', views.customer_edit, name='customer_edit'),
    path('customer/<int:id>/remove', views.customer_delete, name='customer_delete'),

    path('product/<int:id>/view', views.product_view, name='product_view'),

    path('purchase/<int:id>/remove',views.delete_purchase,name='delete_purchase'),

    path('user/<id>/view',views.user_detail, name='user_detail'),

    path('credit-sale',views.credit_sale, name='credit_sale'),
    path('credit-sale_report',views.credit_sale_report, name='credit_sale_report'),

    path('add_opening_stock/<int:id>',views.add_opening_stock,name='add_opening_stock'),
)

