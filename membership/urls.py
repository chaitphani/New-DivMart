from django.urls import path
from .views import main_views as views
from .views import auth_views as auth
from .views import api_views as api_view


urlpatterns = (

    path('home',views.home,name='home-member'),
    path('myclients', views.manage_directs, name='manage_direct'),
    path('transaction/direct',views.direct_transaction,name='direct_transaction'),
    path('transaction/withdrawal',views.withdrawal_transaction,name='withdrawal-transaction'),
    path('transaction/points',views.point_transaction,name='point_transaction'),
    path('request-withdraw',views.withdrawal_request,name='withdrawal_request'),

    path('register',auth.member_signup,name='member-register'),
    path('login', auth.member_login, name='member-login'),
    path('logout', auth.member_logout, name='member-logout'),

    path('points-transaction-api',api_view.PointTransactionView.as_view(),name='PointTransactionView'),
    path('signup', api_view.RegisteredMembersView.as_view(), name='signup'),

    # path("cron-tab", views.CronTest.as_view()),

)