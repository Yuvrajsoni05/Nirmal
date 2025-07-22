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
        noc =  models.IntegerField()
        prpc = models.CharField(max_length=200)
        cylinder_size = models.CharField(max_length=200)
        cylinder_made_in = models.CharField(max_length=200)
        pouch_size = models.CharField(max_length=200)
        pouch_open_size = models.CharField(max_length=200)
        pouch_combination = models.CharField(max_length=200)
        correction = models.TextField()
        image_url = models.URLField()
        
        
class CompanyName(models.Model):
    company_name = models.CharField(max_length=300)
    
