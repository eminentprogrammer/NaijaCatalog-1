from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export.admin import ExportActionModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Account, Institution
# Register your models here.


@admin.register(Account)
class AccountAdmin(BaseUserAdmin, ImportExportModelAdmin, ExportActionModelAdmin):
    list_display = ['email', 'date_joined','last_login']
    ordering = ['email',"last_login"]
    fieldsets = (
        ('User Credentials', {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_librarian','is_active','is_admin','is_staff', 'is_superuser',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields       = ('email',)
    ordering            = ('email','id')
    filter_horizontal   = ()



# @admin.register(StudentProfile)
# class StudentAdmin(admin.ModelAdmin):
#     list_display = ['user','firstname','lastname','contact_no', 'institution', 'institutionID', 'department']



@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display    = ['name', 'contact_email', 'contact_phone', 'location',"date_joined"]
    fieldsets = (
        ('Institutional', {'fields': ('logo','name', 'contact_email', 'contact_phone', 'location', 'gmap')}),
        ('Additional Information',{'fields': ('admin',)}),
    )
    ordering        = ['name']
    list_editable   = ['location']