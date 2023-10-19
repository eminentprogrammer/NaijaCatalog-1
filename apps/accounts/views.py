import json
import uuid
import base64
import time
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, StudentProfile
from .forms import UserRegistration, UpdateProfile, UpdatePasswords, Account

from apps.catalogue.models import Book, Institution
from django.db.models import Q, Count
from django.core.paginator import Paginator
from apps.emailApp.views import send_confirmation_email


# Create your views here.
context = {
    'page_title' : 'Naija Catalog',
}

@login_required
def dashboard_view(request):
    user = request.user
    if user.is_superuser:
        messages.success(request, 'Master Dashboard')
        
        users =  StudentProfile.objects.all()
        institutions = Institution.objects.all()
        context = {
            'users':users,
            'users_count': users.count(),
            'instituions':institutions,
            'instituions_count':institutions.count(),
        }
        return render(request, "users/__dashboard.html", context)
    

    if user.is_student:
        messages.success(request, 'Student Dashboard')
    if user.is_librarian:
        messages.success(request, 'Librarian Dashboard')
    return render(request, "users/__dashboard.html", context)


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
    context = {}
    form = UserRegistration()
    if request.POST:
        token       = request.POST.get('csrfmiddlewaretoken')
        email       = request.POST.get('email')
        username    = request.POST.get('username')
        category    = request.POST.get('category')
        institution = request.POST.get('institution')
        password    = request.POST.get('password')
        
        if not Account.objects.filter(email=email).exists():
            user = Account.objects.create_user(
                email=email,
                username=email,
                password=password
            )

            user = authenticate(email=email, password = password)
            if not user is None:
                stud_obj = StudentProfile.objects.create(user=user, institution=category)
                stud_obj.save()
                login(request, user)
                send_confirmation_email(request, user)
                messages.error(request, f"Welcome {email}")
                return redirect('dashboard')

            messages.error(request, "Account created successfully, log in")
            return redirect("signin")

        context = {
            'email':email,
            # 'username':username,
            'category':category,
            'password':password,
            'institution':institution,
        }       
        messages.error(request, "Email Already exist !!!")
    return render(request, 'users/registrations/register.html', context)
    # return render(request, 'connect-plus/pages/samples/register.html', context=data)






def signIn(request):
    context = {}

    logout(request)
    if request.POST:
        token       = request.POST.get('csrfmiddlewaretoken')
        email       = request.POST.get('email')
        saveauth    = request.POST.get('savelogin')
        password    = request.POST.get('password')

        user = authenticate(email=email, password=password)
        
        if user is not None:
            login(request, user)
            send_confirmation_email(request, user)

            messages.success(request, f"Sign In Successful, welcome back, {user.username}")
            return redirect("dashboard")
        
        else:
            messages.error(request,  "Incorrect email or password")
        
        context = {
            'token':token,
            'email': email,
            'password': password,
            'valid': True,
            'saveauth':saveauth
        }
    return render(request, 'users/registrations/login.html', context)
    # return render(request, 'connect-plus/pages/samples/login.html', context=data)


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
            return redirect("update_profile")
        else:
            context['form'] = form
    
    context['user'] = user
    return render(request, 'users/registrations/update_profile.html', context)



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
            return redirect("update_password")
        else:
            context['form'] = form
    else:
        form = UpdatePasswords(request.POST)
        context['form'] = form
    return render(request,'users/registrations/change_password.html', context)

def reset_password(request):
    context = {}

    if request.POST:
        email = request.POST.get('email')
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email=email)
            messages.success(request, f'Reset link generated, proceed further with the email sent to you @{email}')             
        context['email'] = email
    return render(request, 'users/registrations/reset_password.html', context)


#Logout
def signOut(request):
    user = request.user
    logout(request)
    messages.info(request, f"Thanks {user}")
    return redirect('signin')