from django.shortcuts import render
from .models import *

# Create your views here.

# FRONTEND

def index(request):
    context = {}
    return render(request, 'diverse/index.html', context)

def cart(request):
    context = {}
    return render(request, 'diverse/cart.html', context)

def checkout(request):
    context = {}
    return render(request, 'diverse/checkout.html', context)