from django.shortcuts import render, redirect
from .forms import BookForm
from .models import Book
from apps.accounts.models import Institution, Account
from django.contrib import messages

def CreateBook(request):
    form = BookForm()
    user = request.user

    if request.POST:
        form = BookForm(request.POST)
        if not form.is_valid():
            raise ValueError("Invalid form submitted")
        
        user_obj = Account.objects.get(pk=request.user.pk)
        library_obj = Institution.objects.get(admin=user_obj)
        instance = form.save(commit=False)
        instance.institution = library_obj.name
        instance.save()
        messages.success(request, f"{instance.title}, has been added successfully!")
        return redirect("catalog:create_book")
    
    context = []
    return render(request, 'catalog/createBook.html', locals())


def catalogView(request):
    user_obj = Account.objects.get(pk=request.user.pk)
    library_obj = Institution.objects.get(admin=user_obj)
    catalog = Book.objects.filter(institution=library_obj.name)

    return render(request, 'catalog/list.html', locals())



def single_book_info(request, slug):
    book = Book.objects.get(slug=slug)
    context={
        'book':book,
    }
    return render(request, 'catalog/single_book.html', context)