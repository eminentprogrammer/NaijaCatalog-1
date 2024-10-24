from django.contrib import admin
from .models import Institution
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