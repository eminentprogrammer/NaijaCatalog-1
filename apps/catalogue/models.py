from django.db import models
from django.urls import reverse
from apps.accounts.models import Account, Institution
from django.utils.text import slugify

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
    slug            = models.SlugField(blank=True, null=True, max_length=500)

    # Custom action
    def make_published(self, request, queryset):
        updated_count = queryset.update(status='published')
        self.message_user(request, f'{updated_count} books were marked as published.')
    

    def get_slug(self):
        if not self.slug:
            self.slug = slugify(self.title)
            self.save()
        return slugify(self.title)

    def get_absolute_url(self):
        return reverse('catalog:single_book_info', args=[str(slugify(self.title))])

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.get_slug()
        super().save(*args, *kwargs)

    class Meta:
        verbose_name_plural = "Book Catalogue"


class ExcelUpLoad(models.Model):
    file = models.FileField(upload_to='catalogue/uploads/')
    owner = models.ForeignKey(Institution, default=0,  on_delete=models.PROTECT)
    added = models.BooleanField(default=False)
    date_uploaded = models.DateTimeField(auto_now=True, editable=True)

    class Meta:
        verbose_name_plural = "Excel Upload"

    def __str__(self):
        return str(self.owner)