from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.accounts.models import Institution


@login_required
def partner_portal(request, slug=None):
    context = {}
    if not slug:
        context['partners'] = Institution.objects.all().order_by('name')
        return render(request, 'partner_portal/partners.html', context)
    
    partner = Institution.objects.get(slug=slug)
    context['partner'] = partner
    return render(request, 'partner_portal/index.html', context)
