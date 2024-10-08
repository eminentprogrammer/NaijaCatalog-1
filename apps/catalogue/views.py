import requests
import gscholar
from django.shortcuts import render, redirect
from .forms import BookForm
from .models import Book
from apps.accounts.models import Institution, Account
from django.contrib import messages
from django.utils.text import slugify
from django.contrib import messages
from django.db.models import Q


def search(request):
    context = {}
    combined_query = Q()
    
    for terms, values in request.GET.items():
        context.update({terms: values})

    for queryset in request.GET:
        if request.GET.get(queryset) != "":
            if queryset == 'title' or queryset == 'author' or queryset == 'subject':
                combined_query &= Q(**{f"{queryset}__icontains": request.GET.get(queryset)})
            elif queryset == 'institution':
                combined_query &= Q(**{f"{queryset}": Institution.objects.get(name__icontains=request.GET.get(queryset))})
    try:
        response   = Book.objects.complex_filter(combined_query)
        context.update({'response': response})
        return render(request, 'engine/general_search.html', context)
    except Exception as e:
        print(e)
        return render(request, 'engine/general_search.html', {'error': str(e)})


def advanced_search(request, data):
    pass


def google_scholar_search(request):
    return render(request, 'engine/google_scholar_search.html')


def listBook(request):
    user = request.user
    catalog = Book.objects.filter(institution=user.institution)
    context = {
        'catalog': catalog
    }
    return render(request, 'catalog/listBook.html', context)


def uploadBook(request):
    context = {}
    form = BookForm()
    user = request.user

    if request.POST:
        form = BookForm(request.POST)    
        if form.is_valid():
            institution = Institution.objects.get(admin=user)
            instance = form.save(commit=False)
            instance.institution = institution
            instance.slug = slugify(instance.title)
            instance.save()
            messages.add_message(request, messages.SUCCESS, extra_tags="alert alert-success", message="Book has been added successfully")
            return redirect("catalog:listBook")
        
        messages.add_message(request, messages.ERROR, extra_tags="alert alert-danger", message="Invalid form submitted")

    context['form'] = form
    return render(request, 'catalog/createBook.html', context)


def catalogView(request):
    context = []
    user_obj    = Account.objects.get(pk=request.user.pk)
    library_obj = Institution.objects.get(admin=user_obj)
    catalog     = Book.objects.filter(institution=library_obj.name)

    context = {
        'user': user_obj,
        'library': library_obj,
        'user_catalog': catalog,
    }
    return render(request, 'catalog/list.html', context)



def single_book_info(request, slug):
    context = {}
    try:
        book = Book.objects.filter(slug=slug).first()
        fields_dict = {}
        for field in book._meta.fields:
            if field.name not in ['title','id', 'is_available', 'institution', 'slug'] and getattr(book, field.name) != None:
                fields_dict[field.name] = getattr(book, field.name)

        context["fields_dict"] = fields_dict
        context['partner'] = Institution.objects.get(pk=book.institution.pk)
        context['book'] = book

    except Exception as e:
        messages.info(request, "No Map Loaded")

    context['page_from'] = request.META.get('HTTP_REFERER')
    return render(request, 'catalog/single_book.html', context)



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