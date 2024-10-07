from django.shortcuts import render, redirect
from apps.accounts.models import Institution
from apps.catalogue.models import Book
from apps.catalogue.forms import searchForm
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
