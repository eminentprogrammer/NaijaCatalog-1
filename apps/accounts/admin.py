from django.contrib import admin
from .models import Account, StudentProfile, Institution
# Register your models here.


class AccountAdmin(admin.ModelAdmin):
    list_display = ['email','username', 'date_joined','last_login']
    # readonly_fields = ['password']


class StudentAdmin(admin.ModelAdmin):
    list_display = ['user','firstname','lastname','contact_no', 'institution', 'institutionID', 'department']

class InstitutionAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_email', 'contact_phone', 'location', 'admin']

admin.site.register(Account, AccountAdmin)
admin.site.register(Institution, InstitutionAdmin)
admin.site.register(StudentProfile, StudentAdmin)