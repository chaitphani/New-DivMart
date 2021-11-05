from django.urls import path,include
from useraccount import views

urlpatterns = [
    # path('admin_signup',views.admin_signup,name='admin_signup'),
    # path('cashier_signup',views.cashier_signup,name='cashier_signup'),
    path('common_login',views.common_login,name='common_login'),
    path('admin_logout',views.admin_logout,name='admin_logout'),
    # path('cashier_logout',views.cashier_logout,name='cashier_logout'),
    path('content_types/',views.ContentTypeView.as_view(),name='content_type'),
    path('permissions/',views.PermissionsView.as_view(), name='PermissionsView')

]