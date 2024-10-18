from django.contrib import admin
from .models import Institution, Student
# from unfold.admin import ModelAdmin
# Register your models here.

@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):

    fieldsets = (
    )
    
    add_fieldsets = (
    )

    filter_horizontal   = ()
    
    save_on_top = True
    save_as     = True


@admin.register(Student)
class StudentAdmin(ModelAdmin):
    list_display = ['user', 'institution']
    fieldsets = (
        ('User Credentials', {'fields': ('user',)}),
        ('Additional Information', {'fields': ('institution','slug')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user', 'institution'),
        }),
    )    
    save_on_top = True
    save_as     = True