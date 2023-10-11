import json
import uuid
import base64
import time
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account
from .forms import UserRegistration, UpdateProfile, UpdatePasswords, Account

from apps.catalogue.models import Book
from django.db.models import Q, Count
from django.core.paginator import Paginator

# Create your views here.
context = {
    'page_title' : 'Naija Catalog',
}


@login_required
def dashboard_view(request):
    return render(request, "users/dashboard.html", context)


def dashboard_search(request):
    start_time = time.time()
    context['page_title'] = 'Dashboard'
    search_term = request.GET.get('search')

    # Retrieves all books from the database
    all_books = Book.objects.all().order_by("title")

    # print(type(search_term))
    if search_term is None:
        search_term = ""
    
    if (len(search_term) > 0):
        # Clean Querying Data
        query = request.GET.get('search').replace("'", "").replace('"','')
        # Define option mappings for different search options
        selected_filter = Q(title__icontains=f"{query}") | Q(subject__icontains=f"{query}") | Q(author__icontains=f"{query}")
        queryset = all_books.complex_filter(selected_filter)

        # Create a paginator for the books and get the current page
        paginator = Paginator(queryset, 10)  # Show 4 books per page
        # Get Page
        page = request.GET.get('page')
        # Get the books for the current page
        books = paginator.get_page(page)
        context['queryset'] = books
    else:
        context['queryset'] = ""                 

    end_time = time.time()
    elapsed_time = end_time - start_time
    # Copy the GET parameters and remove the 'page' parameter to generate URL parameters
    get_dict_copy = request.GET.copy()
    params = get_dict_copy.pop('page', True) and get_dict_copy.urlencode()
    
    context['query'] = search_term
    context['elapsed_time'] = elapsed_time
    print(f"Location: {request.build_absolute_uri()}")
    print(f"Query Term: {get_dict_copy}")
    return render(request, "users/dashboard/general_search.html", context)


def signUp(request):
    data = {}
    form = UserRegistration()
    if request.POST:
        token       = request.POST.get('csrfmiddlewaretoken')
        email       = request.POST.get('signup_email')
        username    = request.POST.get('signup_email')
        category    = request.POST.get('category')
        password    = request.POST.get('signup_password')

        form = UserRegistration(request.POST)
        if form.is_valid():
            print("form is valid")
            # email   = form.cleaned_data.get('email')
            # username = form.cleaned_data.get('username')
            # password = form.cleaned_data.get('password1')
            user = Account.objects.create_user(
                email=email,
                username=username,
                password=password
            )
            user = authenticate(email=email, password = password)
            if not user is None:
                login(request, user)
                messages.error(request, f"Welcome {username}")
                return redirect('dashboard')
            
            messages.error(request, "Account created successfully, log in")
            return redirect("login_view")
        else:
            messages.error(request, "Form validation error")

        data = {
            'token':token,
            'email': email,
            'password': hash(password),
            'valid': True
        }
    return render(request, 'users/registrations/register.html', context=data)



def signIn(request):
    data = {}
    logout(request)
    
    if request.POST:
        token = request.POST.get('csrfmiddlewaretoken')
        email = request.POST.get('signin_email')
        password = request.POST.get('signin_password')

        user = authenticate(email=email, password=password)    
        
        if user is not None:
            login(request, user)
            messages.success(request, f"Sign In Successful, welcome {user.username}")
            return redirect("dashboard")
        else:
            messages.error(request,  "Incorrect username or password")

        data = {
            'token':token,
            'email': email,
            'password': hash(password),
            'valid': True
        }
        
    return render(request, 'users/registrations/login.html', context=data)


@login_required
def update_profile(request):
    context['page_title'] = 'Update Profile'
    
    user = Account.objects.get(id = request.user.id)
    
    if not request.method == 'POST':
        form = UpdateProfile(instance=user)
        context['form'] = form
    else:
        form = UpdateProfile(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile has been updated")
            return redirect("accounts:profile")
        else:
            context['form'] = form
            
    return render(request, 'users/management/update_profile.html', context)

@login_required
def update_user(request):
    if request.POST:
        user = Account.objects.get(email=request.user.email)
        username = request.POST.get("username")
        lastname = request.POST.get("last_name")
        firstname = request.POST.get("first_name")
        
        if not Account.objects.filter(username=username).exists():
            user.username = username
            messages.error(request, "Username has already be used !!!")
        
        user.last_name = lastname
        user.first_name = firstname
        user.save()
        user.refresh_from_db()
        messages.success(request, "Profile has been updated")
        return redirect("accounts:user_profile")
    
    return redirect("accounts:user_profile") 


@login_required
def update_password(request):
    context['page_title'] = "Update Password"
    if request.method == 'POST':
        form = UpdatePasswords(user = request.user, data= request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Your Account Password has been updated successfully")
            update_session_auth_hash(request, form.user)
            return redirect("accounts:user_profile")
        
        else:
            context['form'] = form
    else:
        
        form = UpdatePasswords(request.POST)
        context['form'] = form
    return render(request,'users/management/update_password.html', context)


#Logout
def signOut(request):
    user = request.user
    logout(request)
    messages.info(request, f"Thanks {user}, Call Again")
    return redirect('homepage')