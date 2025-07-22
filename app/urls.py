from django.contrib import admin
from django.urls import path,include
from .views import *


urlpatterns = [
    path('',login_page,name='login_page'),
    path('register',register_page,name='register_page'),
    path('logout',user_logout,name='logout'),
    path('dashboard',dashboard_page,name='dashboard_page'),
    path('base',base_html,name='base_html'),
    path('data_entry',data_entry,name='data_entry'),
    path('delete_data/<int:delete_id>/',delete_data,name='delete_data'),
    path('update_data/<int:update_id>/',update_job,name="update_job"),
    path('add_data',add_data,name='add_data'),
    path('profile_page',profile_page,name='profile_page'),
    path('update_profile/<uuid:users_id>/',update_profile,name='update_profile'),
    path('update_password',user_password,name='update_password'),
]
