from django.shortcuts import render
from .models import StreamSource


def home(request):
    context = {
        'sources': StreamSource.objects.all(),
        'title': 'Home'
    }
    return render(request, 'webface/home.html', context)


def about(request):
    return render(request, 'webface/about.html', {'title': 'About'})
