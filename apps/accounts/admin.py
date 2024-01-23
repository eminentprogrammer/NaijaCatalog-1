from django.contrib import admin
from .models import Account, StudentProfile, Institution
# Register your models here.


class AccountAdmin(admin.ModelAdmin):
    list_display = ['email', 'date_joined','last_login']
    readonly_fields = ['password', 'slug']
    ordering = ['email',"last_login"]


class StudentAdmin(admin.ModelAdmin):
    list_display = ['user','firstname','lastname','contact_no', 'institution', 'institutionID', 'department']



class InstitutionAdmin(admin.ModelAdmin):
    list_display    = ['name', 'contact_email', 'contact_phone', 'location',"date_joined"]
    readonly_fields = ['admin','name','slug','contact_email','contact_phone', 'location',]
    ordering        = ['name']
    list_editable   = ['location']



admin.site.register(Account, AccountAdmin)
admin.site.register(Institution, InstitutionAdmin)
admin.site.register(StudentProfile, StudentAdmin)