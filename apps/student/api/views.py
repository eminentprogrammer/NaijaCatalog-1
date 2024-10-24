from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from apps.partners.models import Institution
from ..models import Student

# Create your views here.
User = get_user_model()

@login_required
def dashboard(request):
    user = request.user
    institution = Institution.objects.get(student=user.student)
    context = {
        'institution': institution,
        'user': user,
        'page_title': 'Student Dashboard'
    }
    return render(request, 'students/dashboard.html', context)