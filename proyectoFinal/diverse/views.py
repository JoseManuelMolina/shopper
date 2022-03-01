from django.shortcuts import render
from .models import *
from diverse.models import *

# Create your views here.

# FRONTEND
def page_not_found_view(request, exception):
    return render(request, 'diverse/404.html', status=404)


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

def contacto(request):
    context = {}
    return render(request, 'diverse/contacto.html', context)
    
def faq(request):
    context = {}
    return render(request, 'diverse/faq.html', context)

def enviosDevoluciones(request):
    context = {}
    return render(request, 'diverse/envios-devoluciones.html', context)

def nosotros(request):
    context = {}
    return render(request, 'diverse/nosotros.html', context)

