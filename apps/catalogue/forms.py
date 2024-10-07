from django import forms
from .models import Book


class searchForm(forms.Form):
    title = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'name':'article'}))
    
    class Meta:
        model = None
        fields = ['title']



class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title","author","isbn","edition","call_no","subject","publisher","place_of_publication","year_published"]

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control', 'required': True})
        self.fields['author'].widget.attrs.update({'class': 'form-control', 'required': True})
        self.fields['isbn'].widget.attrs.update({'class': 'form-control', 'required': True})
        self.fields['edition'].widget.attrs.update({'class': 'form-control',})
        self.fields['call_no'].widget.attrs.update({'class': 'form-control', 'required': True})
        self.fields['subject'].widget.attrs.update({'class': 'form-control'})
        self.fields['publisher'].widget.attrs.update({'class': 'form-control'})
        self.fields['place_of_publication'].widget.attrs.update({'class': 'form-control'})
        self.fields['year_published'].widget.attrs.update({'class': 'form-control', 'required': True})