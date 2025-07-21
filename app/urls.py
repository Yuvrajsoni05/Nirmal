from django.contrib import admin
from django.urls import path,include
from .views import *


urlpatterns = [
    path('',login_page,name='login_page'),
    path('register',register_page,name='register_page'),
    path('dashboard',dashboard_page,name='dashboard_page'),
    path('base',base_html,name='base_html'),
    path('data_entry',data_entry,name='data_entry'),
    path('delete_data/<int:delete_id>/',delete_data,name='delete_data'),
    path('update_data/<int:update_id>/',update_job,name="update_job"),
    path('add_data',add_data,name='add_data'),
    path('profile_page',profile_page,name='profile_page')
]
