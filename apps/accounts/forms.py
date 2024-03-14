from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, UserChangeForm
from .models import Account, Institution, StudentProfile


class StudentRegistration(forms.Form):
     university = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Name of Institution'}))
     student_ID = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Student ID'}))
     class Meta:
          model = None
          fields = ['university','student_ID']


class InstitutionRegistration(forms.Form):
     university = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Name of Institution'}))

     class Meta:
          model = Institution
          fields = ['logo', 'name', 'contact_email', 'contact_phone', 'location']

     def save(self, *args, **kwargs):
          if not self.instance.slug:
               from django.utils.text import slugify
               try:
                    self.instance.slug = slugify(self.instance.name)
                    self.instance.save()
               except Exception as e:
                    raise ValueError(e)
          super().save(*args, **kwargs)


class UserRegistration(UserCreationForm):
     email      = forms.EmailField(max_length=250,help_text="The email field is required.")
     class Meta:
          model = Account
          fields = ('email', 'password1', 'password2')


     def clean_email(self):
          email = self.cleaned_data['email']
          try:
               user = Account.objects.get(email = email)
          except Exception as e:
               return email
          raise forms.ValidationError(f"The {user.email} mail is already exists/taken")



class UpdateProfile(UserChangeForm):
     first_name     = forms.CharField(max_length=250, help_text="The First Name field is required.")
     last_name      = forms.CharField(max_length=250, help_text="The Last Name field is required.")
     class Meta:
          model = Account
          fields = ('first_name', 'last_name')


class UpdatePasswords(PasswordChangeForm):
     old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm rounded-0'}), label="Old Password")
     new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm rounded-0'}), label="New Password")
     new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm rounded-0'}), label="Confirm New Password")
     
     class Meta:
          model = Account
          fields = ('old_password','new_password1', 'new_password2')