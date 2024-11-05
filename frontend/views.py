import time
import requests
import gscholar
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from apps.partners.models import Institution
from apps.catalogue.models import Book
from apps.catalogue.api.forms import searchForm
from apps.accounts.api.forms import StudentRegistration, InstitutionRegistration

# Create your views here.

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
            'search':searchForm(),
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

# Define the robots view function
def robots_view(request):
    # Render the robots.txt template
    return render(request, 'robots.txt')


def about(request):
    page = 'about'
    context = {
        'page':page
    }
    return render(request, 'about-us.html', context)

def search_snippet(request):
    combined_query = Q()
    for term in request.GET:
        if term == 'title' or 'author' or 'subject':
            term = term.replace("'", "").replace('"', "")
            if request.GET.get(term) != "":
                combined_query &= Q(**{f"{term}__icontains": request.GET.get(term)})      
    return combined_query


def search(request):
    context = {}
    query = search_snippet(request)
    try:
        response   = Book.objects.complex_filter(query)
        paginator  = Paginator(response, 10)
        page       = request.GET.get("page")
        books      = paginator.get_page(page)
        context['response'] = books
    except Exception as e:
        print(e)

    [context.update({terms: values}) for terms, values in request.GET.items()]
    return render(request, 'frontend/search.html', context)


def advanced_search(request):
    search_term = request.GET.get("search")
    start_time  = time.time()

    if search_term:
        query = search_term.replace("'", "").replace('"', "")
        selected_filter = (
            Q(title__icontains=query) |
            Q(subject__icontains=query) |
            Q(author__icontains=query) |
            Q(institution__icontains=Institution.objects.get(name=query))
        )
        result     = Book.objects.filter(selected_filter)
        paginator = Paginator(result, 10)
        page      = request.GET.get("page")
        books     = paginator.get_page(page)
        context   = {
            "books": books,
            "search_term": search_term,
            "elapsed_time": time.time() - start_time,
        }
        return render(request, "frontend/advanced_search.html", context)

    return render(request, "frontend/advanced_search.html")

def google_scholar_search(request):
    return render(request, 'frontend/google_scholar.html')