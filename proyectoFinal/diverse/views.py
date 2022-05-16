from django.shortcuts import redirect, render

from django.views.generic import ListView, CreateView, UpdateView, TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from diverse.models import *
from account.models import *
from diverse.forms import *

from django.urls import reverse_lazy

# Create your views here.

# FRONTEND
def page_not_found_view(request, exception):
    return render(request, 'diverse/404.html', status=404)

def index(request):
    context = {}
    return render(request, 'diverse/index.html', context)

@login_required(login_url='login')
def perfil(request):
    usuario = request.user
    form = infoPersonal(instance=usuario)

    if request.method == 'POST':
        form = infoPersonal(request.POST, instance=usuario)

        if form.is_valid():
            form.save()
            return redirect('perfil')

    else:
        form = infoPersonal(instance=request.user)
    
    return render(request, 'diverse/perfil.html', {'form':form, 'usuario':request.user})
   

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

