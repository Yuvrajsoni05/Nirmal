from django.contrib import admin
from django.urls import path,include
from .views import *


urlpatterns = [
    path('',login_page,name='login_page'),
    path('register',register_page,name='register_page'),
    path('dashboard',dashboard_page,name='dashboard_page'),
    path('base',base_html,name='base_html'),
    path('data_entry',data_entry,name='data_entry'),
    path('delete_data/<int:delete_id>/',delete_data,name='delete_data')    
]
