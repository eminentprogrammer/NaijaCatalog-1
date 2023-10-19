from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, UserChangeForm
from .models import Account



class StudentRegistration(forms.Form):
     university = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Name of Institution'}))
     student_ID = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Student ID'}))

     class Meta:
          model = None
          fields = ['university','student_ID']


class InstitutionRegistration(forms.Form):
     university = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Name of Institution'}))

     class Meta:
          model = None
          fields = ['university']




class UserRegistration(UserCreationForm):
     email      = forms.EmailField(max_length=250,help_text="The email field is required.")
     username   = forms.CharField(max_length=250,help_text="The username field is required.")
     
     class Meta:
          model = Account
          fields = ('email', 'username', 'password1')


     def clean_email(self):
          email = self.cleaned_data['email']
          try:
               user = Account.objects.get(email = email)
          except Exception as e:
               return email
          raise forms.ValidationError(f"The {user.email} mail is already exists/taken")

     def clean_username(self):
          username = self.cleaned_data['username']
          try:
               user = Account.objects.get(username = username)
          except Exception as e:
               return username
          raise forms.ValidationError(f"The {user.username} mail is already exists/taken")



class UpdateProfile(UserChangeForm):
     first_name     = forms.CharField(max_length=250,help_text="The First Name field is required.")
     last_name      = forms.CharField(max_length=250,help_text="The Last Name field is required.")
     
     class Meta:
          model = Account
          fields = ('first_name', 'last_name')

     def clean_username(self):
          username = self.cleaned_data['username']
          try:
               user = Account.objects.exclude(id=self.cleaned_data['id']).get(username = username)
          except Exception as e:
               return username
          raise forms.ValidationError(f"The {user.username} mail is already exists/taken")
     


class UpdatePasswords(PasswordChangeForm):
     old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm rounded-0'}), label="Old Password")
     new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm rounded-0'}), label="New Password")
     new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm rounded-0'}), label="Confirm New Password")
     
     class Meta:
          model = Account
          fields = ('old_password','new_password1', 'new_password2')