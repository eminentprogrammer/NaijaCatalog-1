# Register your models here.
from django.contrib import admin
from .models import Book, ExcelUpLoad, Institution
from .resources import BookResource
from import_export.admin import ImportExportModelAdmin
from import_export.admin import ExportActionModelAdmin
from django.utils.text import slugify
from django.db.models import F


@admin.register(Book)
class CatalogAdmin(ImportExportModelAdmin, ExportActionModelAdmin):
    list_display   = ["title", 'subject', 'author', 'isbn', 'edition','call_number', 'publisher', 'location', 'institution']
    list_filter    = ['institution','author']
    search_fields  = ['title', 'subject', 'author']

    fieldsets = (
        ('Institution', {
            'fields': ('institution',),
            'classes': ('collapse',)
        }),
        ('Book Information', {
            'fields': ('title', 'subject', 'author', 'edition', 'publisher', 'location', 'year_published')
        }),
        ('Book Access Information', {
            'fields': ('isbn', 'call_number',)
        }),
    )
    import_fields  = ['id', 'title', 'subject', 'author', 'isbn', 'edition','call_number', 'publisher', 'location', 'year_published', 'institution']
    export_fields  = ['id', 'title', 'subject', 'author', 'isbn', 'edition','call_number', 'publisher', 'location', 'year_published', 'institution']

    ordering = ['title']  # Sort by title in ascending order

    # Import/Export options
    resource_class = BookResource

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
          
    def mark_available(self, request, queryset):
        updated_count = queryset.update(is_available=True)
        self.message_user(request, f'{updated_count} books were set available')
          
    def mark_unavailable(self, request, queryset):
        updated_count = queryset.update(is_available=False)
        self.message_user(request, f'{updated_count} books were set unavailable')
          
    def mark_augustineUniversity(self, request, queryset):
        updated_count = queryset.update(institution=Institution.objects.get(id=1).name)
        self.message_user(request, f'{updated_count} books were stored in Augustine University Library Catalog')
    
    mark_pending.short_description = "Mark selected books as pending"
    generate_slug.short_description = "Generate Slugs for Selected Books"
    make_published.short_description = "Mark selected books as published"
    mark_available.short_description = "Mark selected books as available"
    mark_unavailable.short_description = "Mark selected books as unavailable"
    mark_augustineUniversity.short_description = "Mark selected books as Augustine University Materials"
    actions = [make_published, generate_slug, mark_pending, mark_available, mark_unavailable, mark_augustineUniversity]


class ExcelUploadAdmin(admin.ModelAdmin):
    list_display = ['id','owner','file','date_uploaded']
admin.site.register(ExcelUpLoad, ExcelUploadAdmin)