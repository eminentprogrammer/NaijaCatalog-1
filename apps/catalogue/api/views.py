import time
import requests
import gscholar
from django.db.models import Q, Count
from django.contrib import messages
from django.utils.text import slugify
from django.shortcuts import render, redirect

from ..models import Book
from .forms import BookForm, EditBookForm
from apps.partners.models import Institution
from django.core.paginator import Paginator


def upload_book(request):
    """Upload a book to the user's institution's catalog."""
    form = BookForm()
    user = request.user

    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            institution = Institution.objects.get(admin=user)
            book = form.save(commit=False)
            book.institution = institution
            book.slug = slugify(book.title)
            book.save()
            messages.success(request, "Book has been added successfully")
            return redirect("catalog:listBook")
        messages.error(request, "Invalid form submitted")

    context = {
        "form": form,
    }
    return render(request, "catalog/createBook.html", context)

def catalog_view(request):
    """View of all books in the user's institution's catalog."""
    user = request.user
    institution = Institution.objects.get(admin=user)
    books = Book.objects.filter(institution=institution)
    context = {
        "user": user,
        "institution": institution,
        "books": books,
    }
    return render(request, "catalog/list.html", context)

def list_books(request):
    """List all books in a user's institution's catalog."""
    context = {}
    user = request.user

    page_number = request.GET.get("page")
    search_term = request.GET.get("title")

    start_time = time.time()

    try:
        catalog = Book.objects.filter(institution=user.institution).order_by("title")
    except:
        if not user.is_superuser:
            raise ValueError("Invalid institution") 
        catalog = Book.objects.all()

    if search_term:
        messages.add_message(
            request,
            messages.SUCCESS,
            extra_tags="alert alert-success",
            message=f"Search results for: {search_term}",
        )
        catalog = catalog.filter(title__icontains=search_term) 
        end_time = time.time()
        elapsed_time = end_time - start_time
        context['elapsed_time'] = elapsed_time

    paginator  = Paginator(catalog, 10)

    if page_number:
        books     = paginator.get_page(page_number)    
    else: books   = paginator.page(1) 

    context["books"] = books
    context["catalog"] = catalog
    context['paginator'] = paginator
    context["search_term"] = search_term

    return render(request, "catalog/listBook.html", context)


def edit_book_info(request, pk):
    """
    Edit a book in the user's institution's catalog.
    """
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        messages.info(request, "No book found")
        return redirect("catalog:listBook")

    if not request.user == book.institution.admin:
        messages.add_message(
            request,
            messages.ERROR,
            extra_tags="alert alert-danger",
            message="You do not have permission to edit this book",
        )
        return redirect("catalog:single_book_info", slug=book.slug)

    if request.method == "POST":
        form = EditBookForm(request.POST, instance=book)

        if form.is_valid():
            book = form.save(commit=False)
            book.slug = slugify(book.title)
            book.save()
            title = form.cleaned_data["title"]
            messages.add_message(
                request,
                messages.SUCCESS,
                extra_tags="alert alert-success",
                message=f"Book: \"{title}\" has been updated successfully",
            )
            return redirect("catalog:single_book_info", slug=book.slug)

    form = EditBookForm(instance=book)
    context = {
        "form": form,
        "book": book,
        "page_title": "Edit Book",
    }
    return render(request, "catalog/editBook.html", context)


def delete_book(request, pk):
    """
    Delete a book in the user's institution's catalog.
    """
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        messages.info(request, "No book found")
        return redirect("catalog:listBook")
    
    title = book.title
    if request.user == book.institution and request.user.is_superuser:
        book.delete()
        messages.add_message(
            request,
            messages.SUCCESS,
            extra_tags="alert alert-success",
            message=f"Book: \"{title}\" has been deleted successfully",
        )
        return redirect("catalog:listBook")
    else:
        messages.add_message(
            request,
            messages.ERROR,
            extra_tags="alert alert-danger",
            message="You do not have permission to delete this book",
        )
    return redirect("catalog:single_book_info", slug=book.slug)


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
        return render(request, 'search/general_search.html', context)
    except Exception as e:
        print(e)
        return render(request, 'search/general_search.html', {'error': str(e)})

def advanced_search(request):
    """
    Perform an advanced search on the user's institution's catalog.

    The search will query the title, subject, and author fields of the books in the
    user's institution's catalog.

    Args:
        request (HttpRequest): The request object

    Returns:
        HttpResponse: The rendered page with the search results
    """
    user = request.user
    search_term = request.GET.get("search")
    start_time = time.time()

    try:
        books = Book.objects.filter(institution=user.institution).order_by("id","title")
    except:
        if not user.is_superuser:
            raise ValueError("Invalid institution") 
        books = Book.objects.all()

    if search_term:
        query = search_term.replace("'", "").replace('"', "")
        selected_filter = (
            Q(title__icontains=query) |
            Q(subject__icontains=query) |
            Q(author__icontains=query)
        )
        books = books.filter(selected_filter)

    paginator = Paginator(books, 10)
    page = request.GET.get("page")
    books = paginator.get_page(page)
    context = {
        "books": books,
        "search_term": search_term,
        "elapsed_time": time.time() - start_time,
    }
    return render(request, "catalog/listBook.html", context)


def google_scholar_search(request):
    return render(request, 'search/google_scholar_search.html')