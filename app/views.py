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
