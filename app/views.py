from django.shortcuts import get_object_or_404, render,redirect
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.views.decorators.cache import cache_control
from django.views.decorators.cache import cache_control, never_cache
from datetime import datetime
# from torch import t
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout 
import requests 
from django.contrib.auth import update_session_auth_hash
from googleapiclient.http import MediaFileUpload
import json
from decimal import Decimal
from django.core.paginator import Paginator

from django.contrib.sessions.models import Session
from django.utils.timezone import now
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.db.models import Q
from django.db.models import Sum
import tempfile
#  google
from django.core.mail import send_mail
from django.http import JsonResponse
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import mimetypes
import io
import re
import pickle


from django.core.mail import EmailMessage
from pydrive2.auth import GoogleAuth 
from pydrive2.drive import GoogleDrive

#Password

from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetDoneView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
)

# Create your views here.
import os
from django.conf import settings




class CustomPasswordResetView(PasswordResetView):
    template_name = "Password/password_reset_form.html"
    email_template_name = "Password/password_reset_email.html"
    success_url = reverse_lazy("password_reset_done")


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "Password/password_reset_done.html"
    

class CustomPasswordResetConfirm(PasswordResetConfirmView):
    template_name = "Password/password_reset_confirm.html"
    success_url = reverse_lazy("password_reset_complete")


def password_reset_done(request):
    return render(request,'Password/password_update_done.html')

    
    
    
SERVICE_ACCOUNT_FILE = os.path.join(settings.BASE_DIR, 'app', 'Google', 'credentials.json')
SCOPES = ['https://www.googleapis.com/auth/drive']
def login_page(request):    
    if request.method == 'POST':
        username_email = request.POST.get('username')
        password = request.POST.get('password')
        print(username_email)
        print(password)
        
        valid = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',username_email)
        
        if valid:
            user_login = Registration.objects.get(email = username_email.lower()).username
            user = authenticate(request, username=user_login, password=password)
            
        else:
            user = authenticate(request,username=username_email,password=password)
            
        if user is not None:
            login(request, user)
            messages.success(request,'You are Login')
            return redirect('dashboard_page') 
        else:
            messages.error(request,"Invalid Username and Password ",)
            return redirect('login_page')
    return render(request, 'Registration/login_page.html')  


def usernmae_validator(username):
    if len(username) < 3 or len(username) > 12:
        return "Username must be between 3 and 12 character"

def email_validator(email):
    try:
        EmailValidator()(email)
        return "Invalid Email format"
    except ValidationError:
        return "Invalid email formatsss"

def validator_password(password):
    if len(password) < 8:
        return "Password Must be at least 8 characters long"
    
    if not any(char.isupper() for char in password):
        return "Password must contain at least one uppercase "
    if not any(char.islower() for char in password):
         return "Password must contain at least one lowercase"
     
    if not any(char.isdigit() for char in password):
        return "Password must contain at least one number"
    
    if not any(char in "!@#$%^&*()_+-={}[]\\:;\"'<>,.?/~`" for char in password):
        return "Password must contain at least one special character."
    
    
@never_cache
@cache_control(no_store=True, no_cache=True, must_revalidate=True, max_age=0) 
@login_required(redirect_field_name=None)
def register_page(request):
    if not request.user.is_authenticated:
        return redirect('login_page')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')

        email = request.POST.get('emailAddress')
        password = request.POST.get('password')
        confirma_password = request.POST.get('confirma_password')

        required_filed = {
           
            'First Name':first_name,
            'Last Name':last_name, 
            'Username':username,
            'Password':password,
        }
    
        for i , required in required_filed.items():
            if not required:
                messages.error(request,f" {i} field is Required",extra_tags="custom-success-style")
                return redirect('register_page')
        
        email_regex = r"(?!.*([.-])\1)(?!.*([.-])$)(?!.*[.-]$)(?!.*[.-]{2})[a-zA-Z0-9_%+-][a-zA-Z0-9._%+-]*@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_regex, email):
            messages.error(request, "Enter a valid email address.",extra_tags="custom-success-style") 
            return redirect('register_page')
       
        if Registration.objects.filter(username=username).exists():
                messages.error(request,'Username Alredy Exist',extra_tags="custom-success-style")
                return redirect('register_page')
            
        if Registration.objects.filter(email=email).exists():
            messages.error(request,"Email is Alredy Exist",extra_tags="custom-success-style")
            return redirect('register_page')
        
        
        password_error = validator_password(password)
        if password_error:
            messages.error(request,password_error,extra_tags="custom-success-style")
            if password != confirma_password:
                messages.error(request,'Password Confirm Password must be same',extra_tags="custom-success-style")
                return redirect('register_page')

        create_user = Registration.objects.create_user(
            first_name = first_name,
            last_name = last_name,
            username = username,
            password = password,
            email= email,
        )
        create_user.save()
        messages.success(request,"New User Will Created",)
        
        return redirect('edit_user_page')
    return render(request,'Registration/register.html')

@never_cache
@cache_control(no_store=True, no_cache=True, must_revalidate=True, max_age=0)
@login_required(redirect_field_name=None)
def edit_user_page(request):
    if not request.user.is_authenticated:
        return redirect('login_page')
    user_info = Registration.objects.exclude(is_superuser=True).exclude(id=request.user.id).order_by('username')
    context = {
        'users':user_info
    }
    return render(request,'Registration/edit_user.html',context)

@never_cache
@cache_control(no_store=True, no_cache=True, must_revalidate=True, max_age=0)
@login_required(redirect_field_name=None)
def delete_user(request,user_id):
    if not request.user.is_authenticated:
        return redirect('login_page')
    if request.method == 'POST':
        
        Delete_user = get_object_or_404(Registration,id = user_id)
        Delete_user.delete()
       
        messages.success(request,"User Deleted")
        return redirect('edit_user_page')
    
    
@never_cache
@cache_control(no_store=True, no_cache=True, must_revalidate=True, max_age=0)
@login_required(redirect_field_name=None)    
def update_user(request, user_id):
    if not request.user.is_authenticated:
        return redirect('login_page')
    
    try:
        if request.method == 'POST':
            update_user = get_object_or_404(Registration, id=user_id)
            username = request.POST.get('username')
            email = request.POST.get('email')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            
            
            # email_error = email_validator(email)
            # if email_error:
            #     messages.error(request,email_error,extra_tags="custom-success-style")
            #     return redirect('edit_user_page')
            
            
            
            print(user_id)
            required_fields = {
                'Username': username,
                'Firstname': first_name,
                'Lastname': last_name,
                'Email': email,
            }

            for field_name, value in required_fields.items():
                if not value:
                    messages.error(request, f"{field_name} is required.",extra_tags="custom-success-style")
                    return redirect('edit_user_page')
                
                
            email_regex = r"(?!.*([.-])\1)(?!.*([.-])$)(?!.*[.-]$)(?!.*[.-]{2})[a-zA-Z0-9_%+-][a-zA-Z0-9._%+-]*@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            if not re.match(email_regex, email):
                messages.error(request, "Enter a valid email address.",extra_tags="custom-success-style") 
                return redirect('edit_user_page')
                
                
            if username != update_user.username and Registration.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.", extra_tags="custom-success-style")
                return redirect('edit_user_page')


            if email != update_user.email and Registration.objects.filter(email=email).exists():
                messages.error(request, "Email already exists.", extra_tags="custom-success-style")
                return redirect('edit_user_page')

    
            required_fields = {
                'Username': username,
                'Firstname': first_name,
                'Lastname': last_name,
                'Email': email,
            }

            for field_name, value in required_fields.items():
                if not value:
                    messages.error(request, f"{field_name} is required.",extra_tags="custom-success-style")
                    return redirect('edit_user_page')

            if username != update_user.username:
                update_user.username = username
            if email != update_user.email:
                update_user.email = email
        
            update_user.first_name = first_name
            update_user.last_name = last_name
            
            

            logout_user = Registration.objects.get(id=user_id)
            for session in Session.objects.all():
                session_data = session.get_decoded()
                print(session_data)
                if str(session_data.get('_auth_user_id')) == str(logout_user.id):
                    session.delete()
                    
           
           
           
           
            
            update_user.save()

            messages.success(request, "User updated successfully.")
            return redirect('edit_user_page')
    except Exception:
        messages.error(request,"Something went wrong",extra_tags="custom-success-style")
        return redirect('edit_user_page')
        
        
        

@never_cache
@cache_control(no_store=True, no_cache=True, must_revalidate=True, max_age=0)
@login_required(redirect_field_name=None)
def dashboard_page(request):
    if not request.user.is_authenticated:
        return redirect('login_page')
    try:
        
       
            
        get_q = request.GET.get('q')
        date_s = request.GET.get('date')
        cylinder_company = request.GET.get('cylinder_company')

    
        db_sqlite3 = Job_detail.objects.all().order_by('id')
        total_purchse_floats = [] 
        total_purchse = Job_detail.objects.values_list('prpc_purchase')
        for i in total_purchse:
            data_string = i[0]  
            cleaned_string = data_string.replace(",", "")
            float_value = float(cleaned_string)
            total_purchse_floats.append(float_value)

        a = sum(total_purchse_floats)
        print(a)
        total_sell_floats = []
        total_sell = Job_detail.objects.values_list('prpc_sell')
        for  i in total_sell:
            sell_data = i[0]
            cleaned_data = sell_data.replace(",","")
            sell_float = float(cleaned_data)
            total_sell_floats.append(sell_float)
        
        b =  sum(total_sell_floats)
        print(b)
        print(b)
        
        
        filters = Q()

        if get_q:
            filters &= (Q(job_name__icontains=get_q) | Q(company_name__icontains=get_q) | Q(cylinder_made_in__icontains=get_q)
            )

        if date_s:
            filters &= Q(date__icontains=date_s)

        if cylinder_company:
            filters &= Q(cylinder_made_in__icontains=cylinder_company)

        if get_q or date_s or cylinder_company:
            db_sqlite3 = db_sqlite3.filter(filters)

        
        db_sqlite3 = db_sqlite3.order_by('id')
            
        p = Paginator(db_sqlite3, 10)
        page = request.GET.get('page')
        datas = p.get_page(page)
        total_job = db_sqlite3.count()
        company_name = CompanyName.objects.all()
        cylinder_company_names = CylinderMadeIn.objects.all()
        nums = "a" * datas.paginator.num_pages  
        
        
        # sessions = Session.objects.filter(expire_date__gte=now())
    
        # user_ids = [session.get_decoded().get("_auth_user_id") for session in sessions]
        # print(user_ids)
        # active_users = Registration.objects.filter(id__in=user_ids)
        # print(active_users) 

        # active_user_names = [f"{user.first_name} {user.last_name}" for user in active_users]
        # active_users_count = Registration.objects.filter(is_active=True).count()

        # active_users_count = active_users.count()
        # print(user_ids)
        # print(active_user_names)
        # print(active_users_count)

        # data = Job_detail.objects.values_list('prpc_sell')
        # print(data)
        
        


    
        context = {
            'nums': nums,
            'venues': datas,
            'total_job': total_job,
            'company_name': company_name,
            'cylinder_company_names': cylinder_company_names,
            'total_sales':b,
            'total_purchase':a
        }

    except Exception as e:
        print(f"Error: {e}")
        return redirect('dashboard_page')

    return render(request, 'dashboard.html', context)


@never_cache
@cache_control(no_store=True, no_cache=True, must_revalidate=True, max_age=0)
@login_required(redirect_field_name=None)   
def delete_data(request,delete_id):
    if not request.user.is_authenticated:
        return redirect('login_page')
    try:
        
        id = delete_id
        print(id)
        response = requests.delete(f"http://localhost:5678/webhook/d51a7064-e3b9-41f5-a76f-264e19f60b70/artical/delete/{id}")
        data = response.json()
        # print(data)
        messages.success(request,"Job Deleted Sussfully")
        return redirect('dashboard_page')
    except Exception:
        messages.warning(request,"Something went Wrong")
        return redirect('dashboard_page')


@login_required(redirect_field_name=None)  
def base_html(request):
    return render(request,'Base/base.html')


@never_cache
@cache_control(no_store=True, no_cache=True, must_revalidate=True, max_age=0)
@login_required(redirect_field_name=None)
def data_entry(request):
    if not request.user.is_authenticated:
        return redirect('login_page')
    comapny_name = CompanyName.objects.all()
    cylinder_company_names = CylinderMadeIn.objects.all()
    context =  {
        'comapany_name':comapny_name,
        'cylinder_company_names':cylinder_company_names
    }
    return render(request, 'data_entry.html',context)


# def get_drive_services():
#     creds = service_account.Credentials.from_service_account_file(
#         SERVICE_ACCOUNT_FILE, scopes=SCOPES
#     )
#     return build('drive', 'v3', credentials=creds)


# def get_job_name_folder(service,job_name,parent_job_id):
#     query = (
#     f"name='{job_name}' and mimeType='application/vnd.google-apps.folder'and trashed=false and '{parent_job_id}' in parents"
# )
    
#     result = service.files().list(
#         q=query,
#         spaces = 'drive',
#         fields = 'files(id,name)'
#     ).execute()
    
#     folders = result.get('files',[])
    
    
#     if folders:
#         job_id  = folders[0]['id']
#         job_url = f"https://drive.google.com/drive/folders/{job_id}"
#         return job_id , job_url
#     else:
#         folder_metadata = {
#             'name':job_name,
#             'parents': [parent_job_id],
#             'mimeType':'application/vnd.google-apps.folder'
            
#         }
#         job_folder = service.files().create(
#             body = folder_metadata,
#             fields = 'id',
#             supportsAllDrives=True
#         ).execute()
        
        
#         job_id = job_folder.get('id')
#         job_url = f"https://drive.google.com/drive/folders/{job_id}"
#         return job_id,job_url
        

# def get_create_folder(service, folder_name, parent_folder_id,):
#     query = (
#         f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' "
#         f"and trashed=false and '{parent_folder_id}' in parents"
#     )
#     result = service.files().list(
#         q=query,
#         spaces='drive',
#         fields='files(id, name)'
#     ).execute()

#     folders = result.get('files', [])
    
#     if folders:
#         folder_id = folders[0]['id']
#         folder_url = f"https://drive.google.com/drive/folders/{folder_id}"
        
#         return folder_id, folder_url

#     else:
#         # Create new folder
#         folder_metadata = {
#             'name': folder_name,
#             'parents': [parent_folder_id],
#             'mimeType': 'application/vnd.google-apps.folder'
#         }
        
#         folder = service.files().create(
#             body=folder_metadata,
#             fields='id',
#             supportsAllDrives=True
#         ).execute()
        
#         folder_id = folder.get('id')
#         folder_url = f"https://drive.google.com/drive/folders/{folder_id}"
#         return folder_id, folder_url


@login_required(redirect_field_name=None)
def normalize_job_name(job_name):
    return re.sub(r'\s+', ' ', job_name.strip()).lower()

@login_required(redirect_field_name=None)
def check_company_name(company_name):
    return re.sub(r'\s+',' ',company_name.strip()).lower()
          
@login_required(redirect_field_name=None)      
def normalize_cylinder_company_name(cylinder_company_name):
    return re.sub(r'\s+',' ',cylinder_company_name.strip()).lower()

@never_cache
@cache_control(no_store=True, no_cache=True, must_revalidate=True, max_age=0)
@login_required(redirect_field_name=None)
def add_data(request):

    try:
        
        if request.method == 'POST':
            date = request.POST.get('job_date')
            bill_no = request.POST.get('bill_no')
            company_name = request.POST.get('company_name')
            job_name = request.POST.get('job_name')
            job_type = request.POST.get('job_type')
            noc = request.POST.get('noc')
            prpc_purchase = request.POST.get('prpc_purchase')
            prpc_sell = request.POST.get('prpc_sell')
            cylinder_size = request.POST.get('cylinder_size')
            cylinder_made_in_s = request.POST.get('cylinder_select')
            cylinder_date = request.POST.get('cylinder_date')
            cylinder_bill_no = request.POST.get('cylinder_bill_no')
            pouch_size = request.POST.get('pouch_size')
            pouch_open_size = request.POST.get('pouch_open_size')
            pouch_combination_1 = request.POST.get('pouch_combination1')
            pouch_combination_2 = request.POST.get('pouch_combination2')
            pouch_combination_3 = request.POST.get('pouch_combination3')
            pouch_combination_4 = request.POST.get('pouch_combination4')
            new_company = request.POST.get('new_company')
            new_cylinder_company_name = request.POST.get('cylinder_made_in_company_name')
            correction = request.POST.get('correction')
            files = request.FILES.getlist('files') 
            pouch_combination_total  = f"{pouch_combination_1} + {pouch_combination_2} + {pouch_combination_3} + {pouch_combination_4}"
            print(prpc_purchase)
            # print(cylinder_date)
            # print(cylinder_bill_no)
            
       
            if Job_detail.objects.filter(job_name__icontains = job_name,date__icontains  =date).exists():
                    messages.error(request,"Job Name are alredy Exsits on this date  kidnly Update job",extra_tags='custom-success-style')
                    return redirect('data_entry')
            
            
            
            # num_str = prpc_purchase
            # num_str_cleaned = num_str.replace(",", "")  # Remove commas using replace()
            # num_int = int(num_str_cleaned)
            # print(num_int)
            
            # normalized_name = normalize_job_name(job_name)
            # exsting_job_name = Job_detail.objects.all()
            # for i in exsting_job_name:
            #     if normalize_job_name(i.job_name) == normalized_name:
            #         messages.error(request,"Job Name Alredy Exsits",extra_tags="custom-success-style")
            #         return redirect('data_entry')             
            
            
            required_filed = {
                    'Date' :date,
                    'Bill no':bill_no,
                    'Company_Name': company_name,
                    'job name' : job_name,
                    'job type':job_type,
                    'Noc':noc,
                    'Prpc Purchase':prpc_purchase,
                    'Cylinder Size':cylinder_size,
                    'Cylinder Made in':cylinder_made_in_s,
                    'Pouch size':pouch_size,
                    'Pouch Open Size':pouch_open_size,
                    'Cylinder Bill No':cylinder_bill_no,
                    'Cylinder Date':cylinder_date
                    
                    
            }
            for i ,r in required_filed.items():
                if not  r:
                    messages.error(request,f"This {r} Filed Was Required",extra_tags="custom-success-style")
                    return redirect('data_entry')
            
            
            file_dic = {}
            for i ,file in enumerate(files):
                if file.name:
                    file_name_without  = file.name.rsplit('.',1)[0]
                    file_key = f"file_{i}_{file_name_without}"
                else:
                    file_key = f"file_{i}"
                    
                file_dic[file_key] = (file.name, file, file.content_type)
            
            pouch_combination = pouch_combination_total
            if len(files) >= 3: 
                messages.error(request,"You can upload only 2 file",extra_tags="custom-success-style"   )
                return redirect('data_entry')
            
            valid_extension = [".jpeg", ".jpg", ".png" ,".ai"]

            for file in files:
                ext = os.path.splitext(file.name)[1]
                if ext.lower() not in valid_extension:
                    messages.error(request,"Invalid file  Only .jpg, .jpeg, .png and .ai are allowed." ,extra_tags="custom-success-style")
                    return redirect("data_entry")
           
            #     company_name_normalize = check_company_name(company_name)
            #     exsting_company_name  = CompanyName.objects.all()
            #     for i in exsting_company_name:
            #         if check_company_name(i.company_name) == company_name_normalize:
            #             messages.error(request,'Company Name Alredy Exsits',extra_tags='custom-success-style')
            #             return redirect('data_entry')
            if new_company != '':
                
                           
                if CompanyName.objects.filter(company_name__icontains=new_company).exists():
                    messages.error(request,"Company Name Alredy Exists",extra_tags='custom-success-style')
                    return redirect('data_entry')
                add_company = CompanyName.objects.create(
                    company_name=new_company
                )
                add_company.save()
            
           
                company_name = new_company

            # if  new_cylinder_company_name != '':
            #     cylinder_made_in_s = new_cylinder_company_name
            #     cylinder_company_name_normalize = normalize_cylinder_company_name(cylinder_made_in_s)
            #     exsting_cylinder_company_name = CylinderMadeIn.objects.all()
            #     for i in exsting_cylinder_company_name:
            #         if normalize_cylinder_company_name(i.cylinder_made_in) == cylinder_company_name_normalize:
            #             messages.error(request,"Cylinder Company Name Alrdy Exsits",extra_tags='custom-success-style')
            #             return redirect('data-entry')
                                    
                
            if new_cylinder_company_name != '': 
                if CylinderMadeIn.objects.filter(cylinder_made_in__icontains = new_cylinder_company_name).exists():
                    messages.error(request,"Company Name Alredy Exists",extra_tags='custom-success-style')
                    return redirect('data_entry')
                add_new_cylinder_company = CylinderMadeIn.objects.create(
                    cylinder_made_in = new_cylinder_company_name
                )
                add_new_cylinder_company.save()
            
            
                cylinder_made_in_s = new_cylinder_company_name
                

            
            print(cylinder_made_in_s)
                 

            # print(cylinder_made_in_s)
        
            # from django.shortcuts import render, redirect
            # from .models import Company
            # from django.core.exceptions import ValidationError
            # import re

            # def normalize_company_name(name):
            #     return re.sub(r'\s+', ' ', name.strip()).lower()

            # def add_company(request):
            #     error = None
            #     if request.method == 'POST':
            #         name = request.POST.get('name', '')
            #         normalized_name = normalize_company_name(name)

            #         # Check for existing company with same normalized name
            #         existing_companies = Company.objects.all()
            #         for company in existing_companies:
            #             if normalize_company_name(company.name) == normalized_name:
            #                 error = "Company name already exists."
            #                 break

            #         if not error:
            #             Company.objects.create(name=name)
            #             return redirect('success_page')  # replace with your redirect

            #     return render(request, 'add_company.html', {'error': error})

            
            # service = get_drive_services()
            # n8n_folder_id = '14AUzR7EWGbCGoQ-MnIoSabVALt_qUeRS' 

            # folder_id, folder_url = get_create_folder(service, company_name, n8n_folder_id,)
            
            # if folder_id:
            #     print("Folder found/created:", folder_id)
            #     print("Folder URL:", folder_url)
            # else:
            #     print("Error with folder operation")
                
            # job_id , job_url = get_job_name_folder(service,job_name,folder_id)
            
            # if job_id:
            #     print("Job Folder found/created:", job_id)
            #     print("Job Folder URL:", job_url)
            # else:
            #     print("Error with folder operation")
            
            
            # uploaded_file_ids = []
            # for file in files:
            #     temp_file = tempfile.NamedTemporaryFile(delete=False)  # Safe temp file creation
            #     with open(temp_file.name, 'wb+') as destination:
            #         for chunk in file.chunks():
            #             destination.write(chunk)

            #     file_metadata = {
            #         'name': file.name,
            #         'parents': [job_id]  # Correct key is 'parents' not 'parent'
            #     }
            #     media = MediaFileUpload(temp_file.name, mimetype=file.content_type)
            #     uploaded_file = service.files().create(
            #         body=file_metadata,
            #         media_body=media,
            #         fields='id',
            #         supportsAllDrives=True
            #     ).execute()
            
            
            #             data_string = "1 + 1 + 1 + 1"

            # # Split the string by " + " to get a list of number strings
            # numbers_as_strings = data_string.split(" + ")

            # # Convert each string to an integer and assign to separate variables
            # # This assumes you know the exact number of elements beforehand
            # if len(numbers_as_strings) >= 1:
            #     var1 = int(numbers_as_strings[0])
            # if len(numbers_as_strings) >= 2:
            #     var2 = int(numbers_as_strings[1])
            # if len(numbers_as_strings) >= 3:
            #     var3 = int(numbers_as_strings[2])
            # if len(numbers_as_strings) >= 4:
            #     var4 = int(numbers_as_strings[3])

            # # You can also store them in a list if the number of elements varies
            # all_numbers = [int(num) for num in numbers_as_strings]

            # # Print the results to verify
            # print(f"var1: {var1}")
            # print(f"var2: {var2}")
            # print(f"var3: {var3}")
            # print(f"var4: {var4}")
            # print(f"All numbers in a list: {all_numbers}")

            #     uploaded_file_ids.append(uploaded_file.get('id'))
            #     os.remove(temp_file.name) 
            # Gauth=GoogleAuth()
            

                
        data  =  {
                'date':date,
                'bill_no':bill_no,
                'company_name':company_name,
                'job_type':job_type,
                'job_name':job_name,
                'noc':noc,
                'prpc_sell':prpc_sell,
                'prpc_purchase':prpc_purchase,
                'cylinder_size':cylinder_size,
                'cylinder_made_in':cylinder_made_in_s,
                'pouch_size':pouch_size,
                'pouch_open_size':pouch_open_size,
                'pouch_combination':pouch_combination,
                'correction':correction
        }

        response = requests.post('http://localhost:5678/webhook/create-data',data=data,files=file_dic)
        print(response.status_code)
     
        print(response.text)
        data_string  = response.text
        data_dict = json.loads(data_string)
        id_number = data_dict['id']
        print(id_number)
        try:

            
            if response.status_code == 200:
                
                cylinder_data = Job_detail.objects.all().get(id=id_number)
                cylinder_data.cylinder_date = cylinder_date
                cylinder_data.cylinder_bill_no = cylinder_bill_no
                cylinder_data.save()
                
                
                
                messages.success(request,"New Job Create Successfully ")
                return redirect('dashboard_page')
            else:
                db_sql_3 = Job_detail.objects.create(
                    date = data,
                    bill_no = bill_no,
                    company_name = company_name,
                    job_name = job_name,
                    job_type = job_type,
                    noc = noc ,
                    prpc_sell =prpc_sell,
                    prpc_purchase = prpc_purchase ,
                    cylinder_size = cylinder_size,
                    cylinder_made_in = cylinder_made_in_s,
                    pouch_size = pouch_size,
                    pouch_open_size = pouch_open_size,
                    pouch_combination = pouch_combination,
                    correction = correction,
                    
                    
                )
                db_sql_3.save()
                messages.error(request,"Data  Sussfully Add on dbsqlite 3")
                return redirect('dashboard_page')
        except Exception as e:
            messages.error(request,f"Some thing went worng {e}")
            print(e)
            return redirect('data_entry')
    except Exception as e:
        messages.error(request,f"Something went wrong {e}")
        print(e)
        return redirect('data_entry')
    
        
    # else:
    #     messages.error(request,"Something went Wrong")
    #     return redirect('data_entry')
    


@login_required(redirect_field_name=None)      
def  update_job(request,update_id):
    if not request.user.is_authenticated:
        return redirect('login_page')
    try:
        
        if request.method == 'POST':
            date =  request.POST.get('date')
            bill_no = request.POST.get('bill_no')
            company_name = request.POST.get('company_name')
            job_name = request.POST.get('job_name')
            job_type = request.POST.get('job_type')
            noc = request.POST.get('noc')
            prpc_purchase = request.POST.get('prpc_purchase')
            prpc_sell = request.POST.get('prpc_sell')
            cylinder_size = request.POST.get('cylinder_size')
            cylinder_made_in = request.POST.get('cylinder_made_in')
            
            cylinder_date  = request.POST.get('cylinder_date')
            cylinder_bill_no = request.POST.get('cylinder_bill_no')
            
            
            pouch_size = request.POST.get('pouch_size')
            pouch_open_size = request.POST.get('pouch_open_size')
            # pouch_combination = request.POST.get('pouch_combination')
            pouch_combination1 = request.POST.get('pouch_combination1')
            pouch_combination2 = request.POST.get('pouch_combination2')
            pouch_combination3 = request.POST.get('pouch_combination3') 
            pouch_combination4 = request.POST.get('pouch_combination4')
            correction = request.POST.get('correction')
            files = request.FILES.getlist('files')
            
        
            pouch_combination = f"{pouch_combination1} + {pouch_combination2} + {pouch_combination3} + {pouch_combination4}"
            # print(pouch_combination)
            print(prpc_purchase)
            
        
        # print(update_id)
        
        demo = Job_detail.objects.values('date').get(id=update_id)
        date_formatte = demo['date'].strftime("%Y-%m-%d")
       
      
        print(date_formatte)
        
        if date != date_formatte:
            if Job_detail.objects.filter(date = date, job_name =job_name).exists() :
                messages.error(request,"Job is Alredy exists from this date ",extra_tags="custom-success-style")
                return redirect('dashboard_page')

        
        # if Job_detail.objects.filter(date = date, job_name =  job_name):
        #     print("Both Same")
        get_data =  Job_detail.objects.all().get(id=update_id)
      

        get_combinations = get_data.pouch_combination.replace(" ","").split("+")
        # print(get_combinations)
        while len(get_combinations) < 4:
            get_combinations.append('')
            
        # print(get_combinations[0])
        # print(get_combinations[1])
        # print(get_combinations[2])

        data  =  {
            'date':date,
            'bill_no':bill_no,
            'company_name':company_name,
            'job_type':job_type,
            'job_name':job_name,
            'noc':noc,
            'prpc_purchase':prpc_purchase,
             'prpc_sell':prpc_sell,
            'cylinder_size':cylinder_size,
            'cylinder_made_in':cylinder_made_in,
            'pouch_size':pouch_size,
            'pouch_open_size':pouch_open_size,
            'pouch_combination':pouch_combination,
            'correction':correction
        }
        
        
        if len(files) >= 3 :
            messages.error(request,"You can upload only 2 file")
            return redirect('dashboard_page')
        
        
        valid_extension = [".jpeg", ".jpg", ".png" ,".ai"]

        for file in files:
            ext = os.path.splitext(file.name)[1]
            if ext.lower() not in valid_extension:
                messages.error(request,"Invalid file  Only .jpg, .jpeg, .png and .ai are allowed." ,extra_tags="custom-success-style")
                return redirect("dashboard_page")
        
        file_dic = {}
        for i ,file in enumerate(files):
            if file.name:
                file_name_without  = file.name.rsplit('.',1)[0]
                file_key = f"file_{i}_{file_name_without}"
            else:
                file_key = f"file_{i}"
                
            file_dic[file_key] = (file.name, file, file.content_type)
                
                
        
        response = requests.post(f'http://localhost:5678/webhook/7d8dd046-c41e-4f64-8607-caf5f43ddc84/update-data/{update_id}',
                data=data,files=file_dic
            
        )
        if response.status_code == 200:
            
            cylinder_data = Job_detail.objects.all().get(id=update_id)
            cylinder_data.cylinder_date = cylinder_date
            cylinder_data.cylinder_bill_no = cylinder_bill_no
            cylinder_data.save()
            
            
            
            messages.success(request,'Data Updated Sussfully',)
        else:
            messages.error(request,'Something went Wrong',extra_tags="custom-success-style")
     
        return redirect('dashboard_page')
    except Exception as e:
        messages.error(request,f'Something went wrong try again {e}')
        return redirect('dashboard_page')

@login_required(redirect_field_name=None)
def user_logout(request):
    if not request.user.is_authenticated:
        return redirect('login_page')
    
    try:
        logout(request)
        request.session.clear()
        return redirect('login_page')
    except Exception as e:
        messages.error(request,f"Something went Wrong try again {e}")
        return redirect('dashboard_page')

@login_required(redirect_field_name=None)
def profile_page(request):
    if not request.user.is_authenticated:
        return redirect('login_page')
    return render(request,'profile.html')

@login_required(redirect_field_name=None)
def update_profile(request,users_id):
    if not request.user.is_authenticated:
        return redirect('login_page')
    try:
        update_profile = get_object_or_404(Registration,id=users_id)
        if request.method == 'POST':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            email = request.POST.get('email')
        
        
        required_filed = {
            'First Name' :first_name,
            'Last Name':last_name,
            'Email':email,
            'Username':username
        } 
        
        print(users_id)
        for filed,required in required_filed.items():
            if not required:
                messages.error(request,f"{filed} is Required" ,extra_tags="custom-success-style")
                return redirect('profile_page')
            
            
        if email !=  update_profile.email and Registration.objects.filter(email=email).exists():
            messages.error(request,"Email alredy exists" ,extra_tags="custom-success-style")
            return redirect('profile_page')
        
        
        
        
        if username !=  update_profile.username and Registration.objects.filter(username=username).exists():
            messages.error(request,"Username alredy exists",extra_tags="custom-success-style")
            return redirect('profile_page')
        
        
        email_regex = r"(?!.*([.-])\1)(?!.*([.-])$)(?!.*[.-]$)(?!.*[.-]{2})[a-zA-Z0-9_%+-][a-zA-Z0-9._%+-]*@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_regex, email):
            messages.error(request, "Enter a valid email address.",extra_tags="custom-success-style") 
            return redirect('profile_page')
                
            
        
        update_profile.username = username
        update_profile.last_name = last_name
        update_profile.first_name = first_name
        update_profile.email = email
        update_profile.save()
        
        
        
        messages.success(request,"Profile Will Updated",)
        return redirect('profile_page')
    except Exception:
        messages.error(request,'Something went wrong try again')
        return redirect('profile_page')
    
    
    
@login_required(redirect_field_name=None)
def user_password(request):
    if not request.user.is_authenticated:
        return redirect('login_page')
    if request.method == 'POST':
        
        old_password = request.POST.get('old_password').strip()
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        
        if old_password == ''  or old_password == None:
            error = "Please provide Old Password."
            return render (request,'profile.html',context={'error':error})
            
        user_password = request.user
        if not user_password.check_password(old_password):
            messages.error(request,'Old Password is Incorrect',extra_tags='custom-success-style')
            return redirect('profile_page')
        
        
        
        if new_password == ''  or new_password == None:
            errors = "Please provide New Password."
            return render (request,'profile.html',context={'errors':errors})
        
        
       
        
        
        if len(new_password) < 8 or not any(i.isupper() for i in new_password) or not any (i in "!@#$%^&*()_+-={}[]\\:;\"'<>,.?/~`" for i in new_password):
            messages.error(request,"Password Must be 8 Char and One Upercase or one spicial Symboal ",extra_tags='custom-success-style')
            return redirect("profile_page")
                
        if old_password == new_password:
            messages.error(request,"Your Current Passsword or New Password will same Add some Diffrent",extra_tags='custom-success-style')
            return redirect('profile_page')

        if new_password != confirm_password:
            messages.error(request,"new password or confirm Passworsd Must be same ",extra_tags='custom-success-style')
            return redirect("profile_page")
        
        user_password.set_password(new_password)
        user_password.save()
        # messages.success(request,'Password Updated Successfully',)
        print("Password Update")
        # update_session_auth_hash(request,user_password)
        return redirect('login_page')
    
def comapny_add_page(request):
    
    cdr_data = CDRDetail.objects.all()
    
    context = {
        'cdr_details':cdr_data
    }
    return render(request,'CDR/add_company.html',context)


def cdr_add(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        company_email = request.POST.get('company_email')
        cdr_upload_date = request.POST.get('cdr_upload_date')
        cdr_files  =       request.FILES.getlist('cdr_files')

        

        
        if CDRDetail.objects.filter(company_email = company_email).exists():
            messages.error(request,"Company Email is Alredy exists",extra_tags='custom-success-style')
            return redirect('company_add_page')
        
        
        email_regex = r"(?!.*([.-])\1)(?!.*([.-])$)(?!.*[.-]$)(?!.*[.-]{2})[a-zA-Z0-9_%+-][a-zA-Z0-9._%+-]*@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_regex, company_email):
            messages.error(request, "Enter a valid email address.",extra_tags="custom-success-style") 
            return redirect('company_add_page')
        
        cdr_upload =  CDRDetail.objects.create(
                date = cdr_upload_date,
                company_email = company_email,
                company_name = company_name,
                
        )
        
        for cdr_file in cdr_files:
  
            file_name = cdr_file.name
            file_path = os.path.join(settings.MEDIA_ROOT, file_name) 

            os.makedirs(os.path.dirname(file_path), exist_ok=True) 
            with open(file_path, 'wb+') as destination:
                for chunk in cdr_file.chunks():   
                    destination.write(chunk)
            messages.success(request, "New Company Add Successfully")

    return redirect('company_add_page')
    
    
    
def offline_page(request):
    return render(request,'Base/offline_page.html')

from django.core.mail import EmailMultiAlternatives
@login_required(redirect_field_name=None)
def send_mail_data(request):
    if not request.user.is_authenticated:
        return redirect('login_page')
    if request.method == 'POST':
        date = request.POST.get('date')
        bill_no = request.POST.get('bill_no')
        company_name = request.POST.get('company_name')
        company_email_address = request.POST.get('company_address')
        job_name = request.POST.get('job_name')
        noc = request.POST.get('noc')
        prpc_sell = request.POST.get('prpc_sell')
        cylinder_size = request.POST.get('cylinder_size')
        pouch_size = request.POST.get('pouch_size')
        pouch_open_size = request.POST.get('pouch_open_size')
        correction = request.POST.get('correction')
        attachments  = request.FILES.getlist('attachment')
    
    # if len(attachments) >= 3 :
    #             messages.error(request,"You can upload only 2 file")
    #             return redirect('dashboard_page')
    
    print(date,bill_no,company_name,company_email_address,job_name,noc,prpc_sell,cylinder_size,pouch_size,pouch_open_size,correction)
    print(attachments)
    required_field = {
                    'Date' :date,
                    'Bill no':bill_no,
                    'Company_Name': company_name,
                    'job name' : job_name,
                    'Noc':noc,
                    'Cylinder Size':cylinder_size,
                    'Pouch size':pouch_size,
                    'Prpc Sell':prpc_sell,
                    'Pouch Open Size':pouch_open_size,
                    'Company Email Address':company_email_address , 
                    
            }
    for i ,r in required_field.items(): 
        if not  r:
            messages.error(request,f"This {i} Field Was Required",extra_tags="custom-success-style")
            return redirect('dashboard_page')
    
    
    email_regex = r"(?!.*([.-])\1)(?!.*([.-])$)(?!.*[.-]$)(?!.*[.-]{2})[a-zA-Z0-9_%+-][a-zA-Z0-9._%+-]*@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(email_regex, company_email_address):
        messages.error(request, "Enter a valid email address.",extra_tags="custom-success-style")
        
        return redirect('dashboard_page')
    
    
    job_info = {
                "date": date,
                "bill_no": bill_no,
                "company_name": company_name,
                "company_email_address": company_email_address,
                "job_name":job_name,
                "noc":noc,
                "prpc_sell":prpc_sell,
                "cylinder_size":cylinder_size,
                "pouch_size":pouch_size,
                "pouch_open_size":pouch_open_size,
                "correction":correction,

        }
    
    receiver_email = company_email_address
    template_name  = "Base/send_email.html"
    convert_to_html_content =  render_to_string(
    template_name=template_name,
    context=job_info

    )
    email = EmailMultiAlternatives(
    subject="Mail From Nirmal Ventuers",
    body='plain_message',
    from_email=request.user.email,
    to=[receiver_email],

    )
    email.attach_alternative(convert_to_html_content, "text/html")
    for  i in attachments:
        email.attach(i.name, i.read(), i.content_type)
    email.send()
        
    messages.success(request,"Mail Send successfully")
    return redirect('dashboard_page')
    


# def job_detail_print(request,job_id):
#     print(job_id)
    
#     try:
        
#         item = Job_detail.objects.get(id = job_id)
#         data = {
#             'id': item.id,
#             'description': item.correction,
            
#         }
#         return JsonResponse(data)
#     except Job_detail.DoesNotExist:
#             return JsonResponse({'error': 'Item not found'}, status=404)

# email = EmailMessage(
#                 'Subject of the email',
#                 'Body of the email',
#                 'sender@example.com',  # From email address
#                 ['recipient@example.com'], # To email address(es)
#             )

#             # Attach each file
#             for uploaded_file in attachments:
#                 email.attach(uploaded_file.name, uploaded_file.read(), uploaded_file.content_type)

#             email.send()
#             return render(request, 'success.html')
# def check_user_active_session(user_id):
#     try:
#         user = User.objects.get(pk=user_id)  # Retrieve the User object by ID
#     except User.DoesNotExist:
#         # Handle the case where no user with that ID exists
#         return False

#     # Check for active sessions associated with this user
#     sessions = Session.objects.filter(expire_date__gt=datetime.now()) # Filter for active sessions
    
#     for session in sessions:
#         decoded_session = session.get_decoded()  # Decode the session data
#         if decoded_session.get('_auth_user_id') == user.id:  # Check if the session belongs to the given user
#             return True  # User is currently logged in via an active session
    
#     return False


# # views.py

# import os
# import io
# from django.shortcuts import redirect, render
# from django.conf import settings
# from django.core.files.storage import default_storage
# from google_auth_oauthlib.flow import Flow
# from googleapiclient.discovery import build
# from googleapiclient.http import MediaIoBaseUpload
# from django.views.decorators.csrf import csrf_exempt

# # Scopes for Drive
# SCOPES = ['https://www.googleapis.com/auth/drive.file']

# # Temp in-memory user session token storage (for demo)
# user_credentials = {}

# def authorize(request):
#     flow = Flow.from_client_config(
#         {
#             "web": {
#                 "client_id": settings.GOOGLE_OAUTH2_CLIENT_ID,
#                 "client_secret": settings.GOOGLE_OAUTH2_CLIENT_SECRET,
#                 "redirect_uris": [settings.GOOGLE_OAUTH2_REDIRECT_URI],
#                 "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#                 "token_uri": "https://oauth2.googleapis.com/token",
#             }
#         },
#         scopes=SCOPES,
#     )
#     flow.redirect_uri = settings.GOOGLE_OAUTH2_REDIRECT_URI
#     authorization_url, state = flow.authorization_url(
#         access_type='offline',
#         include_granted_scopes='true',
#         prompt='consent'
#     )
#     request.session['state'] = state
#     return redirect(authorization_url)


# def oauth2callback(request):
#     state = request.session['state']
#     flow = Flow.from_client_config(
#         {
#             "web": {
#                 "client_id": settings.GOOGLE_OAUTH2_CLIENT_ID,
#                 "client_secret": settings.GOOGLE_OAUTH2_CLIENT_SECRET,
#                 "redirect_uris": [settings.GOOGLE_OAUTH2_REDIRECT_URI],
#                 "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#                 "token_uri": "https://oauth2.googleapis.com/token",
#             }
#         },
#         scopes=SCOPES,
#         state=state
#     )
#     flow.redirect_uri = settings.GOOGLE_OAUTH2_REDIRECT_URI
#     flow.fetch_token(authorization_response=request.build_absolute_uri())
#     credentials = flow.credentials

#     # Save credentials for later use
#     request.session['credentials'] = {
#         'token': credentials.token,
#         'refresh_token': credentials.refresh_token,
#         'token_uri': credentials.token_uri,
#         'client_id': credentials.client_id,
#         'client_secret': credentials.client_secret,
#         'scopes': credentials.scopes
#     }

#     return redirect('upload_file')


# @csrf_exempt
# def upload_file(request):
#     if request.method == 'POST':
#         file = request.FILES['file']
#         credentials_data = request.session.get('credentials')

#         if not credentials_data:
#             return redirect('authorize')

#         from google.oauth2.credentials import Credentials

#         credentials = Credentials(
#             **credentials_data
#         )

#         service = build('drive', 'v3', credentials=credentials)

#         file_metadata = {'name': file.name}
#         media = MediaIoBaseUpload(file, mimetype=file.content_type)

#         uploaded_file = service.files().create(
#             body=file_metadata,
#             media_body=media,
#             fields='id'
#         ).execute()

#         return render(request, 'upload.html', {
#             'message': f"File uploaded successfully to Google Drive with ID: {uploaded_file.get('id')}"
#         })

#     return render(request, 'upload.html')
       # import re
# from django.shortcuts import redirect
# from django.contrib import messages
# from .models import CDRDetail
# from .google_drive_service import get_drive_service, create_company_folder


# def cdr_add(request):
#     if request.method == 'POST':
#         company_name = request.POST.get('company_name')
#         company_email = request.POST.get('company_email')
#         cdr_upload_date = request.POST.get('cdr_upload_date')
#         cdr_files = request.FILES.getlist('cdr_files')  # assuming multiple files

#         # Validate required fields
#         required_fields = {
#             'Company Name': company_name,
#             'Company Email': company_email,
#             'Upload Date': cdr_upload_date,
#         }

#         for field_name, value in required_fields.items():
#             if not value:
#                 messages.error(request, f'{field_name} is required.')
#                 return redirect('company_add_page')

#         # Check for existing email
#         if CDRDetail.objects.filter(company_email=company_email).exists():
#             messages.error(request, "Company Email already exists.", extra_tags='custom-success-style')
#             return redirect('company_add_page')

#         # Validate email format
#         email_regex = r"(?!.*([.-])\1)(?!.*([.-])$)(?!.*[.-]$)(?!.*[.-]{2})[a-zA-Z0-9_%+-][a-zA-Z0-9._%+-]*@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
#         if not re.match(email_regex, company_email):
#             messages.error(request, "Enter a valid email address.", extra_tags="custom-success-style")
#             return redirect('company_add_page')

#         # Create database record
#         cdr_upload = CDRDetail.objects.create(
#             date=cdr_upload_date,
#             company_email=company_email,
#             company_name=company_name
#         )

#         # Google Drive folder creation
#         try:
#             service = get_drive_service()
#             parent_folder_id = 'YOUR_PARENT_FOLDER_ID'  # Replace with your actual parent folder ID
#             folder_id, folder_link = create_company_folder(service, company_name, parent_folder_id)

#             # Save folder link
#             cdr_upload.google_drive_folder = folder_link
#             cdr_upload.save()
#         except Exception as e:
#             messages.error(request, f"Google Drive folder creation failed: {str(e)}")
#             return redirect('company_add_page')

#         messages.success(request, "New company added successfully.")
#         return redirect('company_add_page')

#     return redirect('company_add_page')


# import os
# import pickle
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build

# SCOPES = ['https://www.googleapis.com/auth/drive.file']

# def get_drive_service():
#     creds = None
#     if os.path.exists('token.pickle'):
#         with open('token.pickle', 'rb') as token:
#             creds = pickle.load(token)

#     if not creds or not creds.valid:
#         flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
#         creds = flow.run_local_server(port=0)
#         with open('token.pickle', 'wb') as token:
#             pickle.dump(creds, token)

#     return build('drive', 'v3', credentials=creds)


# def create_company_folder(service, company_name, parent_folder_id=None):
#     file_metadata = {
#         'name': company_name,
#         'mimeType': 'application/vnd.google-apps.folder',
#     }
#     if parent_folder_id:
#         file_metadata['parents'] = [parent_folder_id]

#     folder = service.files().create(body=file_metadata, fields='id').execute()
#     folder_id = folder.get('id')
#     folder_link = f"https://drive.google.com/drive/folders/{folder_id}"
#     return folder_id, folder_link
