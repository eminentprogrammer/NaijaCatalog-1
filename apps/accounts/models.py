import uuid
import random
from django.urls import reverse
from django.contrib import messages
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# Create your models here.


class MyAccountManager(BaseUserManager):
         
    def create_user(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        
        email = email.lower()
        user = self.model(email=self.normalize_email(email), username=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password, **extra_fields):

        if not email:
            raise ValueError("Email is required")
        
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_superuser", True)
    
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
    
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")
    
        return self.create_user(email, username, password, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    email           = models.EmailField(unique=True)
    username        = models.CharField(max_length=100, unique=True)

    is_active       = models.BooleanField(default=True)    
    is_student      = models.BooleanField(default=False)
    is_admin        = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_librarian     = models.BooleanField(default=False)
    is_superuser    = models.BooleanField(default=False)
    
    date_joined     = models.DateTimeField(auto_now_add=True, editable=True)
    last_login      = models.DateTimeField(verbose_name='last login', auto_now=True, editable=True)

    slug            = models.CharField(max_length=200, blank=True, null=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']
    

    objects = MyAccountManager()
    class Meta:
        verbose_name_plural = "Account Manager"
        ordering            = ['-date_joined']
    
    def __str__(self):
        return self.email   

    def get_full_name(self):
        return f"{self.last_name} {self.first_name}"

    def get_username(self):
        return str(self.username.capitalize())

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        self.is_admin = True
        return self.is_admin
    
    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True
    
    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = uuid.uuid4()

        super().save(*args, **kwargs)


class Institution(models.Model):
    logo            = models.ImageField(blank=True, null=True)
    name            = models.CharField(max_length=500)
    location        = models.CharField(max_length=500)
    contact_email   = models.EmailField(blank=True)
    contact_phone   = models.CharField(max_length=15, blank=True) 
    slug            = models.SlugField(blank=True, null=True)
    admin           = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='Librarian')

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

 
class StudentProfile(models.Model):
    image           = models.ImageField(blank=True, null=True)
    firstname       = models.CharField(max_length=200, blank=True)
    lastname        = models.CharField(max_length=200, blank=True)
    contact_no      = models.CharField(max_length=15, blank=True)
    institutionID   = models.CharField(max_length=20, blank=True)
    institution     = models.CharField(max_length=500, blank=True)
    department      = models.CharField(max_length=100, blank=True)
    is_active       = models.BooleanField(default=False)
    user            = models.OneToOneField(Account, on_delete=models.CASCADE, related_name="student")

    class Meta:
        verbose_name_plural = "Students"
    
    def __str__(self):
        return self.user.email