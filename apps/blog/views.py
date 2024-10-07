from django.shortcuts import render
# Create your views here.


def blog(request):
    # Create a context dictionary with the page variable
    page = "blog"
    context = {
        'page':page
    }
    # Render the news.html template with the context
    return render(request, 'blog/news.html', context)