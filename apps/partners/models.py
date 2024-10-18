import cloudinary
from django.urls import reverse
from django.db import models
from django.contrib.auth import get_user_model
from cloudinary.models import CloudinaryField

class Institution(models.Model):
    logo            = CloudinaryField("NaijaCatalog/institution/logo/", blank=True, null=True)
    name            = models.CharField(max_length=500, blank=True)
    short_name      = models.CharField(max_length=10, blank=True)  
    location        = models.CharField(max_length=500, blank=True)
    contact_email   = models.EmailField(blank=True)
    contact_phone   = models.CharField(max_length=15, blank=True)

    gmap            = models.CharField(blank=True, max_length=1000)
    is_active       = models.BooleanField(default=True)
    date_joined     = models.DateField(auto_now_add=True)

    slug            = models.SlugField(blank=True, null=True)

    admin           = models.OneToOneField("accounts.Account", on_delete=models.CASCADE, related_name='institution', blank=True, null=True)

    class Meta:
        verbose_name_plural = "Institutions"
    
    def get_absolute_url(self):
        return reverse('partner_portal', args=[str(self.slug)])

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            try:
                self.slug = slugify(self.name)
                self.save()
            except Exception as e:
                raise ValueError(e)
            
        super().save(*args, **kwargs)    

    def __str__(self):
        return str(self.name)
    
from uuid import uuid4

class Student(models.Model):
    institution = models.OneToOneField(Institution, on_delete=models.CASCADE, related_name='student')
    user        = models.OneToOneField("accounts.Account", on_delete=models.CASCADE, related_name='student')
    slug        = models.SlugField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Students"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = uuid4()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('student_portal', args=[str(self.institution.slug)])
    
    def __str__(self):
        return self.user.email