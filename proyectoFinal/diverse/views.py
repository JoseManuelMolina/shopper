from django.shortcuts import render
from .models import *
from diverse.models import *

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

def catalogoH(request):
    context = {
        "sexo" : "hombre"
    }
    return render(request, 'diverse/catalogo.html', context)

def catalogoM(request):
    context = {
        "sexo" : "mujer"
    }
    return render(request, 'diverse/catalogo.html', context)

def catalogoNo(request):
    context = {
        "sexo" : "niño"
    }
    return render(request, 'diverse/catalogo.html', context)

def catalogoNa(request):
    context = {
        "sexo" : "niña"
    }
    return render(request, 'diverse/catalogo.html', context)