import re
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, UserChangeForm
from apps.accounts.models import Account
from apps.partners.models import Institution

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
     email      = forms.EmailField(max_length=250, help_text="The email field is required.")
     class Meta:
          model = Account
          fields = ['email', 'password1', 'password2']


     def clean_email(self):
          email = self.cleaned_data['email']
          try:
               user = Account.objects.get(email = email)
          except Exception as e:
               return email
          raise forms.ValidationError(f"The {user.email} mail is already exists/taken")



class UpdateProfileForm(UserChangeForm):
     first_name     = forms.CharField(max_length=250, help_text="The First Name field is required.")
     last_name      = forms.CharField(max_length=250, help_text="The Last Name field is required.")
     class Meta:
          model = Account
          fields = ('email',)


class UpdatePasswords(PasswordChangeForm):
     old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm rounded-0'}), label="Old Password")
     new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm rounded-0'}), label="New Password")
     new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm rounded-0'}), label="Confirm New Password")
     
     class Meta:
          model = Account
          fields = ('old_password','new_password1', 'new_password2')


class UpdateInstitutionForm(forms.ModelForm):
     name = forms.CharField(label='Name of Institution', widget=forms.TextInput(attrs={'class':'form-control', 'name':'institution'}))
     short_name = forms.CharField(label='Shortname', widget=forms.TextInput(attrs={'class':'form-control'}))
     contact_email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class':'form-control', 'name':'email'}))
     contact_phone = forms.CharField(label='Phone', widget=forms.TextInput(attrs={'class':'form-control', 'name':'phone'}))
     location = forms.CharField(label='Location', widget=forms.TextInput(attrs={'class':'form-control', 'name':'location'}))
     
     def clean(self):
          cleaned_data = super().clean()
          email = cleaned_data.get('contact_email')
          phone = cleaned_data.get('contact_phone')
          cleaned_phone = ''.join(char for char in phone if char.isdigit())

          EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
          if email and not re.match(EMAIL_REGEX, email):
               raise forms.ValidationError("Please enter a valid email address")


          PHONE_REGEX = r'^(\+?1-?)?(?:\d{3})[\s.-]?(?:\d{3})[\s.-]?\d{4}$'
          if bool(re.match(PHONE_REGEX, cleaned_phone)):
               raise forms.ValidationError("Please enter a valid phone number")
        
     def save(self, commit=True):
          instance = super().save(commit=False)
          if commit:
               instance.save()
               instance.refresh_from_db()
          return instance
     
     class Meta:
          model = Institution
          fields = ['name','short_name', 'contact_email', 'contact_phone', 'location']


class UploadInstitutionLogoForm(forms.ModelForm):
     logo = forms.ImageField(label='logo', widget=forms.FileInput(attrs={'class':'form-control'}))

     class Meta:
          model = Institution
          fields = ['logo',]
