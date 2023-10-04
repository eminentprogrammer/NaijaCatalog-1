from django.db import models
from apps.accounts.models import Account, Institution


class Book(models.Model):
    title           = models.CharField(max_length=200, blank=True)
    author          = models.CharField(max_length=200, blank=True)
    series          = models.CharField(max_length=200, blank=True)
    subject         = models.CharField(max_length=200, blank=True)
    isbn            = models.CharField(max_length=200, blank=True, verbose_name="ISBN")
    publisher       = models.CharField(max_length=200, blank=True)
    location        = models.CharField(max_length=200, blank=True, verbose_name="Publisher Location")
    call_number     = models.CharField(max_length=200, blank=True, verbose_name="Call Number")
    institution     = models.CharField(max_length=200, blank=True, verbose_name="Institution Hosted")
    year_published  = models.DateField(editable=True)
    date_uploaded   = models.DateField(auto_now_add=True, editable=True)
    is_available    = models.BooleanField(default=True)

    # Custom action
    def make_published(self, request, queryset):
        updated_count = queryset.update(status='published')
        self.message_user(request, f'{updated_count} books were marked as published.')

    class Meta:
        verbose_name_plural = "Book Catalogue"

    def __str__(self):
        return self.title



class ExcelUpLoad(models.Model):
    file = models.FileField(upload_to='catalogue/uploads/')
    owner = models.ForeignKey(Institution, default=0,  on_delete=models.PROTECT)
    added = models.BooleanField(default=False)
    date_uploaded = models.DateTimeField(auto_now=True, editable=True)

    class Meta:
        verbose_name_plural = "Excel Upload"

    def __str__(self):
        return str(self.owner)