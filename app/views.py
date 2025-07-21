from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth import login, authenticate, logout
import requests 
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




def register_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        phone_number = request.POST.get('phoneNumber')
        email = request.POST.get('emailAddress')
        password = request.POST.get('password')
        confirma_password = request.POST.get('confirma_password')
        
        
        print(username)
        
        
        if Registration.objects.filter(email=email).exists():
            print("Email is Alredy Exist")
        
        if password !=  confirma_password:
            print('Password Confirm Password must be same')
        

        create_user = Registration.objects.create_user(
            first_name = first_name,
            last_name = last_name,
            username = username,
            password = password,
            email= email,
            
            
        )
        create_user.save()
        
        return redirect('register_page')
    return render(request,'Registration/register.html')

def dashboard_page(request):
   
    response = requests.get("http://localhost:5678/webhook/get-data")
    data = response.json()
    
    if not data:
        data = []
    context = {
        'data':data,
        
    }
    
    return render(request,'dashboard.html',context)


def delete_data(request,delete_id):
    id = delete_id
    print(id)
    response = requests.delete(f"http://localhost:5678/webhook/d51a7064-e3b9-41f5-a76f-264e19f60b70/artical/delete/{id}")
    data = response.json()
    print(data)
    return redirect('dashboard_page')
    
def base_html(request):
    return render(request,'Base/base.html')


def data_entry(request):
    return render(request, 'data_entry.html')

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
        
        print(date)
    
    
    
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
    
    
    response = requests.post('http://localhost:5678/webhook/create-data',data=data)
    return redirect ('data_entry')
        
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
    
    response = requests.post(f'http://localhost:5678/webhook/7d8dd046-c41e-4f64-8607-caf5f43ddc84/update-data/{update_id}',
            data=data,
           
    )
    
    return redirect('dashboard_page')


def profile_page(request):
    return render(request,'profile.html')