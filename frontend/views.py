import requests
import gscholar
from django.shortcuts import render, redirect
from apps.accounts.models import Institution
from apps.catalogue.models import Book
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from apps.accounts.forms import StudentRegistration, InstitutionRegistration
# Create your views here.



def support(request):
    return render(request, "support.html")


def about(request):
    page = 'about'
    context = {
        'page':page
    }
    return render(request, 'about-us.html', context)


# Define the news view function
def news(request):
    # Create a context dictionary with the page variable
    page = "news"
    context = {
        'page':page
    }
    # Render the news.html template with the context
    return render(request, 'news.html', context)

# Define the robots view function
def robots_view(request):
    # Render the robots.txt template
    return render(request, 'robots.txt')

# Define the homepage view function
def homepage(request):
    # Initialize an empty context dictionary
    context = {}
    # Set the page variable to 'homepage'
    page = "homepage"
    # Try to retrieve books and institutions from the database
    try:
        # Retrieve all books and order them by title, author, and subject
        books = Book.objects.all().order_by('title','author','subject')[:4]
        # Retrieve all institutions
        institutions = Institution.objects.all()
        # Create a context dictionary with the necessary variables
        context = {
            'page': page,
            'search':search,
            'studform':  StudentRegistration(),
            'Instiform': InstitutionRegistration(),
            'books': books,
            'institutions':institutions,
        }
        # Render the homepage template with the context dictionary
        return render(request, 'homepage.html', context)
    # If an exception occurs, print the error message and render the homepage template without any context
    except Exception as e:
        print(e)
    return render(request, 'homepage.html')

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
    query = request.GET.get('article')
    # if not request.user.is_authenticated:
    #     messages.success(request, f"Sign in to use the search functionality")
    #     return redirect("homepage")    
    if query:
        try:
            querysets   = Book.objects.filter(title__icontains=query)
            # obj         = gscholar.query(query)
            # scholar     = convertJ(obj)
            # context['gscholar'] = scholar
            context = {'query':query, 'querysets':querysets}                    
        except Exception as e:
            print(e)
        return render(request, 'engine/general_search.html', context)
    
    return render(request, 'engine/general_search.html')


def google_scholar_search(request):
    return render(request, 'engine/google_scholar_search.html')