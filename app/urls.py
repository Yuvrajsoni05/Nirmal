from django.contrib import admin
from django.urls import path,include
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',login_page,name='login_page'),
    path('register',register_page,name='register_page'),
    path('logout',user_logout,name='logout'),
    path('edit_user',edit_user_page,name='edit_user_page'),
    path('dashboard',dashboard_page,name='dashboard_page'),
    path('base',base_html,name='base_html'),
    path('data_entry',data_entry,name='data_entry'),
    path('delete_data/<int:delete_id>/',delete_data,name='delete_data'),
    path('update_data/<int:update_id>/',update_job,name="update_job"),
    path('add_data',add_data,name='add_data'),
    path('profile_page',profile_page,name='profile_page'),
    path('update_profile/<uuid:users_id>/',update_profile,name='update_profile'),
    path('update_password',user_password,name='update_password'),
    
    path('delete_user/<uuid:user_id>/',delete_user,name='delete_user'),
    path('update_user/<uuid:user_id>/',update_user,name="update_user"),
    
    path('company_add_page',comapny_add_page,name='company_add_page'),
    path('new_cdr_upload',cdr_add,name='new_cdr_upload'),
    path('delete_cdr/<int:delete_id>/',cdr_delete,name='delete_cdr'),
    path('update_cdr/<int:update_id>/',cdr_update,name='update_cdr'),
    
    
    path('offline_page',offline_page,name='offline-page'),
    
    path('send_mail',send_mail_data,name='send_mail'),
    
    # path('print_job/<int:job_id>/',job_detail_print,name='job_detail_print'),
    
    path('password_reset',CustomPasswordResetView.as_view(),name="password_reset"),
    path('password_reset_done/',CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>',CustomPasswordResetConfirm.as_view(),name="password_reset_confirm"),
    path('reset_done',password_reset_done , name="password_reset_complete"),
    
]
