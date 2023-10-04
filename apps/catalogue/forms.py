from django import forms
from .models import Book


class searchForm(forms.Form):
    article = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'name':'article'}))
    
    class Meta:
        model = None
        fields = ['article']



class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ["title","author","isbn","series","call_number","subject","publisher","location","year_published"]