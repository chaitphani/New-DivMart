from os import name
from django.contrib import admin
from django.urls import path,include
from apis.views import *
from rest_framework.authtoken import views

urlpatterns = (

    path('api-token-auth/', views.obtain_auth_token),
    # path('adminusers/',AdminListCreateView.as_view(), name='adminusers'),
    # path('adminusers/<int:id>',AdminDetailUpdateDelView.as_view(),name='admindetails'),
    path('staffusers/', StaffListCreateView.as_view(),name='staffusers'),
    # path('staffusers/<int:id>', StaffDetailUpdateDelView.as_view(),name='staffdetails'),
    path('banks',BankCreation.as_view(),name='bankccreation'),
    path('banks/<int:id>', BankDetailUpdateDelView.as_view(),name='bankdetails'),
    path('products/',ProductListCreateView.as_view(),name='productdetails'),
    path('products/<int:id>',ProductDetailUpdateDelView.as_view(),name='productdetails'),
    path('categories/',CategoryListCreateView.as_view(),name='vcategories'),
    path('categories/<int:id>',CategoryDetailUpdateDelView.as_view(),name='categorydetails'),
    path('brands/',BrandListCreateView.as_view(),name='brands'),
    path('brands/<int:id>',BrandDetailUpdateDelView.as_view(),name='branddetails'),
    path('units/',UnitsListCreateView.as_view(),name='units'),
    path('units/<int:id>',UnitsDetailUpdateDelView.as_view(),name='unitsdetails'),
    path('subcategories/',SubcatListCreateView.as_view(),name='subcategories'),
    path('suppliers/',SupplierListCreateView.as_view(),name='suppliers'),
    path('suppliers/<int:id>',SupplierDetailUpdateDelView.as_view(),name='supplierdetails'),
    path('customergroups/',CustomerGroupListCreateView.as_view(),name='customergroups'),
    path('customers/',CustomerListCreateView.as_view(),name='customers'),
    path('customers/<int:id>',CustomerDetailUpdateDelView.as_view(),name='cusomerdetails'),
    path('purchases/',PurchaseListCreateView.as_view(),name='purchases'),
    path('purchases/<int:id>',PurchaseDetailUpdateDelView.as_view(),name='purchasedetails'),
    # path('purchases/<product_name>',PurchaseReturnUpdateDelView.as_view(),name='purchasreturnedetails'),
    path('sells/<int:id>',SellDetailUpdateDelView.as_view(),name='sellldetails'),
    path('expenses/',AddExpensesView.as_view(),name='expenses'),
    path('expcategories/',AddExpensesCategoryView.as_view(),name='expcategories'),
    path('expcategories/<int:id>',AddExpensesDetailUpdateDelView.as_view(),name='expcategories'),
    path('purchaseinfo/<int:id>',PurchaseInfosDetailUpdateDelView.as_view(),name='purchaseinfo'),
    path('payments/<int:id>',PayementView.as_view(),name='payments'),


    # from my side..

    path('sells/',SellListCreateView.as_view(),name='sells'),
    path('barcode_api', ProductBarCode.as_view(), name='barcodes'),
    path('barcode_api/<barcode_no>', ProductsByBarcode.as_view(), name='barcode'),

)