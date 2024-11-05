from django.urls import reverse
from django.db import models
from apps.partners.models import Institution
# Create your models here.

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