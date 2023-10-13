# Register your models here.
from django.contrib import admin
from .models import Book, ExcelUpLoad
from .resources import BookResource
from import_export.admin import ImportExportModelAdmin
from import_export.admin import ExportActionModelAdmin
from django.utils.text import slugify

class CatalogAdmin(ImportExportModelAdmin, ExportActionModelAdmin):
    list_display   = ["title", 'subject', 'author', 'isbn', 'series','call_number', 'publisher', 'location', 'institution']
    search_fields  = ['title', 'author']

    list_filter    = ['institution','author']
    search_fields  = ['title', 'subject', 'author']

    import_fields  = ['id', 'title', 'subject', 'author', 'isbn', 'series','call_number', 'publisher', 'location', 'year_published', 'institution']
    export_fields  = ['id', 'title', 'subject', 'author', 'isbn', 'series','call_number', 'publisher', 'location', 'year_published', 'institution']

    ordering = ['title']  # Sort by title in ascending order

    # Export options
    resource_class = BookResource

    # Custom action
    def make_published(self, request, queryset):
        updated_count = queryset.update(status='published')
        self.message_user(request, f'{updated_count} books were marked as published.')
     
    def mark_pending(self, request, queryset):
        updated_count = queryset.update(status='pending')
        self.message_user(request, f'{updated_count} books were marked as pending.')
          
    def mark_available(self, request, queryset):
        updated_count = queryset.update(is_available=True)
        self.message_user(request, f'{updated_count} books were set available')
          
    def mark_unavailable(self, request, queryset):
        updated_count = queryset.update(is_available=False)
        self.message_user(request, f'{updated_count} books were set unavailable')
          
    def mark_augustineUniversity(self, request, queryset):
        updated_count = queryset.update(institution="Augustine University Ilara-Epe, Lagos")
        self.message_user(request, f'{updated_count} books were stored in Augustine University Library Catalog')
    

    mark_pending.short_description = "Mark selected books as pending"
    make_published.short_description = "Mark selected books as published"
    mark_available.short_description = "Mark selected books as available"
    mark_unavailable.short_description = "Mark selected books as unavailable"
    mark_augustineUniversity.short_description = "Mark selected books as Augustine University Materials"
    actions = [make_published, mark_pending, mark_available, mark_unavailable, mark_augustineUniversity]

admin.site.register(Book, CatalogAdmin)


class ExcelUploadAdmin(admin.ModelAdmin):
    list_display = ['id','owner','file','date_uploaded']

admin.site.register(ExcelUpLoad, ExcelUploadAdmin)