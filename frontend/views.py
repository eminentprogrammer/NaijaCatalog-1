import requests
import gscholar
from django.shortcuts import render, redirect
from apps.accounts.models import Institution
from apps.catalogue.models import Book
from django.contrib import messages
from apps.accounts.forms import StudentRegistration, InstitutionRegistration
# Create your views here.

def homepage(request):
    context = {}
    books = Book.objects.all().order_by('title','author','subject')[:4]
    institutions = Institution.objects.all()
    
    context = {
        'search':search,
        'studform': StudentRegistration(),
        'Instiform':InstitutionRegistration(),
        'books':books,
        'institutions':institutions,
    }
    return render(request, 'homepage.html', context)


def convertJ(obj):
    import re
    citation_str = obj
    # Define a regular expression pattern to match key-value pairs
    pattern = r'(\w+)={([^{}]+)}'
    # Use re.findall to extract all key-value pairs
    matches = re.findall(pattern, citation_str)
    # Create a dictionary from the matches
    citation_dict = {key: value for key, value in matches}
    # Now, citation_dict contains the citation information as a dictionary
    return citation_dict


def search(request):
    context = {}
    if not request.user.is_authenticated:
        messages.success(request, f"Sign in to use the search functionality")
        return redirect("homepage")
    
    query = request.GET.get('article')
    try:
        querysets = Book.objects.filter(title__icontains=query)
        obj = gscholar.query(query)
        scholar = convertJ(obj)
        context['gscholar'] = scholar
        
    except Exception as e:
        print(e)
    context = {
        'query':query,
        'querysets':querysets,
    }
    return render(request, 'engine/general_search.html', context)


def google_scholar_search(request):
    return render(request, 'engine/google_scholar_search.html')