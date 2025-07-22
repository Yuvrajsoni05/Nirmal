from django.shortcuts import get_object_or_404, render,redirect
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout 
import requests 
from django.contrib.auth import update_session_auth_hash
# Create your views here.

def login_page(request):    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            
            login(request, user)  

            return redirect('dashboard_page') 
            
    return render(request, 'Registration/login_page.html')  

@login_required(redirect_field_name=None)
def register_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')

        email = request.POST.get('emailAddress')
        password = request.POST.get('password')
        confirma_password = request.POST.get('confirma_password')
        
        
        
        required_filed = {
           
            'first_name':first_name,
            'last_name':last_name, 
            'username':username,
            'password':password,
        }
        
        
        for i , required in required_filed.items():
            if not required:
                messages.error(request,f"This  {i}  {required} field is Required",extra_tags="custom-success-style")
                return redirect('register_page')
            
            
        
        if Registration.objects.filter(username=username).exists():
                messages.error(request,'Username Alredy Exist',extra_tags="custom-success-style")
                return redirect('register_page')
            
        if Registration.objects.filter(email=email).exists():
            messages.error(request,"Email is Alredy Exist",extra_tags="custom-success-style")
            return redirect('register_page')
        
        
        if len(password) < 8 or not any(i.isupper() for i in password) or not any (i in "!@#$%^&*()_+-={}[]\\:;\"'<>,.?/~`" for i in password):
            messages.error(request,"Password  must be at least 8 character with one uppercase and one spical charchter",extra_tags="custom-success-style")
            return redirect('register_page')
        
        
        
        if password !=  confirma_password:
            messages.error(request,'Password Confirm Password must be same')
        

        create_user = Registration.objects.create_user(
            first_name = first_name,
            last_name = last_name,
            username = username,
            password = password,
            email= email,
        )
        create_user.save()
        messages.success("New User Will Created")
        
        return redirect('register_page')
    return render(request,'Registration/register.html')

@login_required(redirect_field_name=None)
def dashboard_page(request):
   
    response = requests.get("http://localhost:5678/webhook/get-data")
    data = response.json()
    total_job = Job_detail.objects.all().count()
    if not data:
        data = []
    context = {
        'data':data,
        'total_job':total_job
    }
    
    return render(request,'dashboard.html',context)

@login_required(redirect_field_name=None)
def delete_data(request,delete_id):
    id = delete_id
    print(id)
    response = requests.delete(f"http://localhost:5678/webhook/d51a7064-e3b9-41f5-a76f-264e19f60b70/artical/delete/{id}")
    data = response.json()
    print(data)
    return redirect('dashboard_page')


@login_required(redirect_field_name=None)  
def base_html(request):
    return render(request,'Base/base.html')

@login_required(redirect_field_name=None)
def data_entry(request):
    
    comapny_name = CompanyName.objects.all()
    
    context =  {
        'comapany_name':comapny_name
    }
    return render(request, 'data_entry.html',context)

@login_required(redirect_field_name=None)
def add_data(request):
    if request.method == 'POST':
        date =  request.POST.get('job_date')
        bill_no = request.POST.get('bill_no')
        company_name = request.POST.get('company_name')
        job_name = request.POST.get('job_name')
        job_type = request.POST.get('job_type')
        noc = request.POST.get('noc')
        prpc = request.POST.get('prpc')
        cylinder_size = request.POST.get('cylinder_size')
        cylinder_made_in = request.POST.get('cylinder_made_in')
        pouch_size = request.POST.get('pouch_size')
        pouch_open_size = request.POST.get('pouch_open_size')
        pouch_combination = request.POST.get('pouch_combination')
        correction = request.POST.get('correction')
        files = request.FILES.getlist('files')
        
        print(date)

        file_dic = {}
        
        for i ,file in enumerate(files):
            if file.name:
                file_name_without  = file.name.rsplit('.',1)[0]
                file_key = f"file_{i}_{file_name_without}"
            else:
                file_key = f"file_{i}"
                 
            file_dic[file_key] = (file.name, file, file.content_type)
        
    db_add = Job_detail.objects.create(
        date =  date,
        bill_no = bill_no,
        company_name = company_name,
        job_name = job_name,
        job_type = job_type,
        noc = noc,
        prpc = prpc,
        cylinder_size = cylinder_size,
        cylinder_made_in = cylinder_made_in,
        pouch_size = pouch_size,
        pouch_open_size = pouch_open_size,
        pouch_combination = pouch_combination,
        correction = correction,
        
        )
    db_add.save()
    messages.success(request,"Data Will Sussfully Add on db.sqlite3",extra_tags="custom-success-style")
    
    data  =  {
        'date':date,
        'bill_no':bill_no,
        'company_name':company_name,
        'job_type':job_type,
        'job_name':job_name,
        'noc':noc,
        'prpc':prpc,
        'cylinder_size':cylinder_size,
        'cylinder_made_in':cylinder_made_in,
        'pouch_size':pouch_size,
        'pouch_open_size':pouch_open_size,
        'pouch_combination':pouch_combination,
        'correction':correction
    }
    
    
    
    
    
    response = requests.post('http://localhost:5678/webhook/create-data',data=data,files=file_dic)
    
    return redirect ('data_entry')


@login_required(redirect_field_name=None)      
def  update_job(request,update_id):
    if request.method == 'POST':
        date =  request.POST.get('job_date')
        bill_no = request.POST.get('bill_no')
        company_name = request.POST.get('company_name')
        job_name = request.POST.get('job_name')
        job_type = request.POST.get('job_type')
        noc = request.POST.get('noc')
        prpc = request.POST.get('prpc')
        cylinder_size = request.POST.get('cylinder_size')
        cylinder_made_in = request.POST.get('cylinder_made_in')
        pouch_size = request.POST.get('pouch_size')
        pouch_open_size = request.POST.get('pouch_open_size')
        pouch_combination = request.POST.get('pouch_combination')
        correction = request.POST.get('correction')
        files = request.FILES.getlist('files')
        

    data  =  {
        'date':date,
        'bill_no':bill_no,
        'company_name':company_name,
        'job_type':job_type,
        'job_name':job_name,
        'noc':noc,
        'prpc':prpc,
        'cylinder_size':cylinder_size,
        'cylinder_made_in':cylinder_made_in,
        'pouch_size':pouch_size,
        'pouch_open_size':pouch_open_size,
        'pouch_combination':pouch_combination,
        'correction':correction
    }
    
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
    return redirect('dashboard_page')


@login_required(redirect_field_name=None)
def user_logout(request):
    logout(request)
    return redirect('login_page')

@login_required(redirect_field_name=None)
def profile_page(request):
    return render(request,'profile.html')


def update_profile(request,users_id):
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
    for filed,required in required_filed.items():
        if not required:
            messages.error(request,f"{filed} is Required" ,extra_tags='custom-success-style')
            return redirect('profile_page')
        
    update_profile = get_object_or_404(Registration,id=users_id)
    update_profile.username = username
    update_profile.last_name = last_name
    update_profile.first_name = first_name
    update_profile.email = email
    
    
    update_profile.save()
    messages.success(request,"Profile Will Updated",extra_tags='custom-success-style')
    return redirect('profile_page')
    
def user_password(request):
    if request.method == 'POST':
        
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        user_password = request.user
        if not user_password.check_password(old_password):
            messages.error(request,'Old Password is Incorrect',extra_tags='custom-success-style')
            return redirect("profile_page")
        if len(new_password) < 8 or not any(i.isupper() for i in new_password) or not any (i in "!@#$%^&*()_+-={}[]\\:;\"'<>,.?/~`" for i in new_password):
            messages.error(request,"Password Must be 8 Char and One Upercase or one spicial Symboal ",extra_tags='custom-success-style')

        if new_password != confirm_password:
            messages.error(request,"new password or confirm Passworsd Must be same ",extra_tags='custom-success-style')
        
        user_password.set_password(new_password)
        user_password.save()
        messages.success(request,'Password Updated Successfully',extra_tags='custom-success-style')
        
        update_session_auth_hash(request,user_password)
        return redirect('profile_page')