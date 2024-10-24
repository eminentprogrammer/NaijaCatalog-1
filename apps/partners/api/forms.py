from django import forms
from apps.student.models import Student
from ..models import Institution
from apps.accounts.models import Account

class StudentRegistration(forms.ModelForm):
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class':'form-control form-control-sm rounded-0'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'type':'password','class':'form-control form-control-sm rounded-0'}), label="Password")

    class Meta:
        model = Account
        format_name = 'Student Registration'
        fields = ['email','password']

    def validate(self, email):
        if Account.objects.filter(email = email).exists():
            raise forms.ValidationError("The email entered does not exist")
        return True
    
    def validate_email(self, email):
        try:
            user = Account.objects.get(email__iexact = email)
        except Account.DoesNotExist:
            raise forms.ValidationError("The email entered does not exist")