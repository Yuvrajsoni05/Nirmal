from django.contrib import admin
from .models import *
# Register your models here.



admin.site.register(CylinderMadeIn)




class AdminDetail(admin.ModelAdmin):
    list_display = ("first_name" ,"last_name" , "email","username")
admin.site.register(Registration,AdminDetail)



class AdminJobDetails(admin.ModelAdmin):
    list_display = ("date", "bill_no" , "company_name" , "job_name" , "prpc_purchase" , "prpc_sell")
admin.site.register(Job_detail,AdminJobDetails)



class AdminCompanyDetail(admin.ModelAdmin):
    list_display  = ["id" ,"company_name"]
admin.site.register(CompanyName,AdminCompanyDetail)


class AdminCDRDetail(admin.ModelAdmin):
    list_display = ["id" , 'company_name']
admin.site.register(CDRDetail,AdminCDRDetail)

    
# class AdminCompanyName(admin.ModelAdmin):
#     list_display = ("company_name")
# admin.site.register(CompanyName,AdminCompanyName)