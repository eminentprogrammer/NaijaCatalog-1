from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export.admin import ExportActionModelAdmin
from .models import Account
from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from django.contrib.auth.admin import UserAdmin
from django import forms


@admin.register(Account)
class AccountAdmin(UserAdmin, ImportExportModelAdmin, ExportActionModelAdmin):
    email = forms.EmailField(label="", widget=forms.EmailInput(attrs={'class': 'form-control'}))

    list_display = ['email', 'date_joined','last_login']
    ordering = ['email',"last_login"]

    fieldsets = (
        ('User Credentials', {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active','is_admin','is_staff', 'is_superuser','is_student','is_librarian',)})
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    search_fields       = ('email',)
    ordering            = ('email',)
    filter_horizontal   = ()
    ordering = ("email",)
    
    save_on_top = True
    save_as     = True
    form        = UserChangeForm
    add_form    = UserCreationForm
    change_password_form = AdminPasswordChangeForm