import json
import uuid
import base64
import time
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Institution
from .forms import UserRegistration, UpdateProfileForm, UpdatePasswords, Account, InstitutionRegistration, UpdateInstitutionForm
from apps.catalogue.models import Book
from django.db.models import Q, Count
from django.core.paginator import Paginator

from apps.emailApp.views import send_confirmation_email

# Create your views here.
context = {
    'page_title' : 'Naija Catalog',
}




@login_required
def dashboard(request):
    return render(request, 'users/institution/dashboard.html', context)


@login_required
def dashboard_redirect(request):
    user = request.user
    if user.is_librarian:
        return redirect('library_dashboard')
    # elif user.is_superuser:
        # return redirect('admin:index')
    else:
        return redirect('student_dashboard')

@login_required
def institutionDashboard(request):
    user = request.user
    context = {

    }
    return render(request, 'users/institution/dashboard.html', context)


@login_required
def studentDashboard(request):
    user = request.user
    context = {

    }
    return render(request, 'users/student/dashboard.html', context)


@login_required
def dashboard_view(request):
    user = request.user
    messages.success(request, 'Master Dashboard')
    return render(request, "users/__dashboard.html", locals())


@login_required
def dashboard_search(request):
    user = request.user

    start_time = time.time()
    context['page_title'] = 'Dashboard'
    search_term = request.GET.get('search')

    # Retrieves all books from the database based on the Institution
    all_books = Book.objects.filter(institution=user.institution).order_by("title")

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
    # print(f"Location: {request.build_absolute_uri()}")
    # print(f"Query Term: {get_dict_copy}")
    return render(request, "users/dashboard/general_search.html", context)


def institutionRegistration(request):
    logout(request)
    context = {}

    if request.POST:
        email       = request.POST['email']
        institution = request.POST['institution']
        password    = request.POST['password']
        
        if not Account.objects.filter(email=email).exists():
            user = Account.objects.create_user(
                email       = email,
                password    = password
            )
            user.is_librarian = True
            user.save()
            user.refresh_from_db()

            user = authenticate(email=email, password = password)
            institution = Institution.objects.create(
                name=institution, 
                contact_email=user.email,
                admin=user)
            institution.refresh_from_db()

            if not user is None:
                login(request, user)
                messages.add_message(request, messages.SUCCESS, extra_tags="alert alert-success", message="Account created successfully, log in")
                return redirect('update_profile')

            messages.add_message(request, messages.ERROR, extra_tags="alert alert-danger", message="Account not created")
            return redirect("signin")
        else:
            messages.error(request, "Account already exists")
            return redirect("signin")

    form = UserRegistration()
    context['form'] = form
    return render(request, 'users/registrations/institution_registration.html', context)



def signUp(request):
    logout(request)
    context = {}
    form = UserRegistration()

    if request.POST:
        email       = request.POST.get('email')
        category    = request.POST.get('category')
        institution = request.POST.get('institution')
        password    = request.POST.get('password')
        
        if not Account.objects.filter(email=email).exists():
            user = Account.objects.create_user(
                email       = email,
                password    = password
            )
            user.save()
            user = authenticate(email=email, password = password)

            if not user is None:
                login(request, user)
                # send_confirmation_email(request, user)
                messages.error(request, f"Welcome {email}")
                return redirect('dashboard')
            messages.error(request, "Account created successfully, log in")

            return redirect("signin")
        else:
            context = {
                'email':email,
                'category':category,
                'password':password,
                'institution':institution,
            }
            messages.error(request, "Email Already exist !!!")
            return render(request, 'users/registrations/register.html', context)
        
    institutions = Institution.objects.all().only("name","pk")
    context['institutions'] = institutions
    return render(request, 'users/registrations/register.html', locals())
    

def signIn(request):
    logout(request)
    context = {}

    if request.POST:
        token       = request.POST.get('csrfmiddlewaretoken')
        email       = request.POST.get('email')
        saveauth    = request.POST.get('savelogin')
        password    = request.POST.get('password')

        user = authenticate(email=email, password=password)
        
        if user is not None:
            login(request, user)
            # res = send_confirmation_email(request, user)
            messages.add_message(request, messages.SUCCESS, extra_tags="alert alert-success", message="Sign In Successful")
            return redirect("dashboard")
        else:
            messages.error(request,  "Incorrect email or password")

        context = {
            'token'     :token,
            'email'     : email,
            'password'  : password,
            'valid'     : True,
            'saveauth'  :saveauth
        }
    return render(request, 'users/registrations/login.html', context)



@login_required
def update_profile(request):
    context = {'page_title': 'Update Profile'}
    user = request.user
    
    if user.is_librarian:
        form = UpdateInstitutionForm(instance=user.institution)
    else:
        form = UpdateProfileForm(instance=user)

    if request.POST:
        form = UpdateInstitutionForm(request.POST, instance=Institution.objects.get(admin=user))

        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, extra_tags="alert alert-success", message="Profile has been updated")
            return redirect("update_profile")
        
        else:
            messages.add_message(request, messages.SUCCESS, extra_tags="alert alert-warning", message="Profile not updated")
    context['form'] = form    
    return render(request, 'users/registrations/update_profile.html', context)



@login_required
def update_user(request):
    if request.POST:
        user = Account.objects.get(email=request.user.email)
        lastname = request.POST.get("last_name")
        firstname = request.POST.get("first_name")
        
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