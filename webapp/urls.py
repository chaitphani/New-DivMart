from django.urls import path
from . import views


urlpatterns = (

    path('',views.home, name='web_home'),
    path('about',views.about, name='about'),
    path('categories',views.categories, name='web_categories'),
    path('feedback',views.feedback, name='feedback'),
    path('contact',views.contact, name='contact'),
    path('PrivacyPolicy',views.privacy_policy, name='privacy_policy'),
    path('Terms&Conditions',views.terms_conditions, name='terms_conditions'),

)