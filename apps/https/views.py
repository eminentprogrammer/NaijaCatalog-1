from django.shortcuts import render

global template_name 
template_name = "https/handler.html"


def handler400(request, exception):
    message = "Bad request"
    code = 400
    return render(request, template_name, locals())

def handler403(request, exception):
    message = "Permission Denied"
    code  = 403
    return render(request, template_name, locals())

def handler404(request, exception):
    message = "Page Not Found"
    code = 404
    return render(request, template_name, locals())

def handler500(request):
    message = "Internal Server Error"
    code = 500
    return render(request, template_name, locals())