from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
# Create your models here.
class Registration(AbstractUser):
    
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True
    )

    first_name = models.CharField(max_length=200, blank=True,null=True,)
    last_name = models.CharField(max_length=200,blank=True, null=True)
    email = models.EmailField(max_length=200, unique=True,)


class Job_detail(models.Model):
        date = models.DateField()
        bill_no = models.CharField(max_length=200)
        company_name = models.CharField(max_length=300)
        job_name = models.CharField(max_length=200)
        job_type  = models.CharField(max_length=200)
        noc =  models.TextField(blank=True, null=True)
        prpc_purchase = models.CharField(max_length=200)
        prpc_sell = models.CharField(max_length=200,blank=True, null=True)
        cylinder_size = models.CharField(max_length=200)
        cylinder_made_in = models.CharField(max_length=200)
        pouch_size = models.CharField(max_length=200)
        pouch_open_size = models.CharField(max_length=200)
        pouch_combination = models.CharField(max_length=200)
        correction = models.TextField(blank=True, null=True)
        folder_url = models.URLField()
        image_links = models.CharField(max_length=1000,blank=True, null=True)
        cylinder_date = models.DateField(blank=True, null=True)
        cylinder_bill_no = models.CharField(blank=True, null=True)
        
        
        
        
class CompanyName(models.Model):
    # date = models.DateField(auto_now_add=True,blank=True, null=True)
    company_name = models.CharField(max_length=300,unique=True,)
    # job_name = models.CharField(max_length=200,blank=True, null=True)
    # file_url = models.models.URLField(max_length=200,blank=True, null=True)
    
    
    
class CylinderMadeIn(models.Model):
    cylinder_made_in =  models.CharField(max_length=300,unique=True,blank=True, null=True)
    
    

class CDRDetail(models.Model):
    date = models.DateField()
    company_name = models.CharField(max_length=200)
    job_name =  models.CharField(max_length=200,blank=True, null=True)
    company_email = models.EmailField(blank=True, null=True,unique=True)
    # cdr_upload = models.FileField(upload_to='cdr_file/',blank=True, null=True)
    file_url = models.URLField(max_length=200,blank=True, null=True)
    image_url = models.URLField(max_length=900,blank=True, null=True)
    
     
     
