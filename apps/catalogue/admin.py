# Register your models here.
from django.contrib import admin
from .models import Book, ExcelUpLoad, Institution
from .api.resources import BookResource
from django.utils.text import slugify
from django.db.models import F

from import_export.admin import ExportActionMixin, ImportExportMixin
# from unfold.admin import ModelAdmin
# from unfold.contrib.import_export.forms import ExportForm, ImportForm, SelectableFieldsExportForm

@admin.register(Book)
class CatalogAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display   = ["title", 'subject', 'author', 'isbn', 'edition','call_no', 'publisher', 'place_of_publication', 'institution']
    list_filter    = ['institution', 'author']
    search_fields  = ['title', 'subject', 'author', 'slug']

    fieldsets = (
        ('Institution', {
            'fields': ('institution',),
            'classes': ('collapse',)
        }),
        ('Book Information', {
            'fields': ('title', 'subject', 'author', 'edition', 'publisher', 'place_of_publication', 'year_published')
        }),
        ('Book Access Information', {
            'fields': ('isbn', 'call_no',)
        }),
        ('Others', {
            'fields': ('slug',)
        }),

    )
    ordering = ['id']  # Sort by title in ascending order

    # Import/Export options
    resource_class    = BookResource
    # import_form_class = ImportForm
    # export_form_class = ExportForm
    # export_form_class = SelectableFieldsExportForm


    # Custom action
    def make_published(self, request, queryset):
        updated_count = queryset.update(status='published')
        self.message_user(request, f'{updated_count} books were marked as published.')

    def generate_slug(self, request, queryset):
        updated_count = 0
        for instance in queryset:
            # Assuming 'title' is the field you want to slugify
            instance.slug = slugify(instance.title)  
            instance.save()
        updated_count +=  1
        # updated_count = queryset.update(slug=slugify(queryset['book']))
        self.message_user(request, f'{updated_count} books slug were generated.')
     
    def mark_pending(self, request, queryset):
        updated_count = queryset.update(status='pending')
        self.message_user(request, f'{updated_count} books were marked as pending.')
                          
    def mark_augustineUniversity(self, request, queryset):
        updated_count = queryset.update(institution=Institution.objects.get(id=1).name)
        self.message_user(request, f'{updated_count} books were stored in Augustine University Library Catalog')
    
    mark_pending.short_description = "Mark selected books as pending"
    generate_slug.short_description = "Generate Slugs for Selected Books"
    make_published.short_description = "Mark selected books as published"
    mark_augustineUniversity.short_description = "Mark selected books as Augustine University Materials"
    actions = [make_published, generate_slug, mark_pending, mark_augustineUniversity]


@admin.register(ExcelUpLoad)
class ExcelUploadAdmin(admin.ModelAdmin):
    list_display = ['id','owner','file','date_uploaded']