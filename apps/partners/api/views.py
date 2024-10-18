from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.partners.models import Institution
from .forms import StudentRegistration
from ..models import Student
from django.contrib import messages
from apps.accounts.models import Account



# Create your views here.
@login_required
def student_view(request):
    """
    Student View: For creating student profile for a particular institution
    Method:
        GET: Return a form to create a student profile
        POST: Create a student profile and associate it with the institution
    Note: This view is only accessible to logged in users who are not students and who have a valid institution
    """
    context = {}
    form = StudentRegistration()
    institution = request.user.institution
    students    = Student.objects.filter(institution=institution)

    if request.POST:
        form = StudentRegistration(request.POST)
    
        if Student.objects.filter(institution=institution).exists():
            messages.add_message(request, messages.ERROR, extra_tags="alert alert-warning", message="Student Profile already exists")
            return redirect('student_view')
        
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            
            if not form.validate(email):
                messages.add_message(request, messages.ERROR, extra_tags="alert alert-warning", message="Email already exists")
                return redirect('student_view')
            
            student_instance = Account.objects.create_user(email=email, password=password)
            student_instance.is_student = True
            student_instance.save()
        
            # Create a student object and associate it with the institution
            Student.objects.create(institution=institution, user=student_instance)
            messages.add_message(request, messages.SUCCESS, extra_tags="alert alert-success", message="Profile has been created successfully")
            return redirect('student_view')
        else:
            messages.add_message(request, messages.ERROR, extra_tags="alert alert-warning", message="Profile not created")
            return redirect('student_view')
    
    context['form'] = form
    context['students'] = students
    return render(request, 'partners/student.html', context)


@login_required
def student_list(request):
    institution = request.user.institution
    students    = Student.objects.filter(institution=institution)
    return render(request, 'partners/student.html', {'students': students})



def student_portal(request, slug):
    institution = get_object_or_404(Institution, slug=slug)
    return render(request, 'partners/portal.html')


@login_required
def partners(request):
    context = {}
    context['partners'] = Institution.objects.all().order_by('name')
    return render(request, 'partners/partners.html', context)

@login_required
def partnerInfo(request, slug=None):
    context = {}
    context['partner'] = Institution.objects.get(slug=slug)
    return render(request, 'partners/index.html', context)