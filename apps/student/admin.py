from django.contrib import admin
from .models import Student

# Register your models here.
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
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