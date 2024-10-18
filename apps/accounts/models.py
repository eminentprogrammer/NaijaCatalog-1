import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from apps.partners.models import Institution

class MyAccountManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        
        email = email.lower()
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        if user.is_librarian:
            institution_instance = Institution.objects.get_or_create(admin=user)
            institution_instance.save()
        
        user.save(using=self._db)
        return user


    def create_superuser(self, email, password, **extra_fields):
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

        return self.create_user(email, password, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    email           = models.EmailField(unique=True)

    is_active       = models.BooleanField(default=True)  
    is_admin        = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)    
    is_superuser    = models.BooleanField(default=False)
    is_librarian    = models.BooleanField(default=False)
    is_student      = models.BooleanField(default=False)
    
    date_joined     = models.DateTimeField(auto_now_add=True, editable=True)
    last_login      = models.DateTimeField(verbose_name='last login', auto_now=True, editable=True)

    slug            = models.CharField(max_length=200, blank=True, null=True)
    
    USERNAME_FIELD  = "email"
    # REQUIRED_FIELDS = []
    
    objects         = MyAccountManager()

    class Meta:
        verbose_name_plural = "Account Manager"
        ordering            = ['-date_joined']
    
    def __str__(self):
        return self.email

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        self.is_admin = True
        return self.is_admin
    
    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True
    
    def save(self, *args, **kwargs):
        if self.slug != "":
            self.slug = uuid.uuid4()
        super().save(*args, **kwargs)