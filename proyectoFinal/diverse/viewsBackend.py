from django.shortcuts import render

# Create your views here.

# BACKEND

def index(request):
    context = {}
    return render(request, 'diverseBackend/index.html', context)