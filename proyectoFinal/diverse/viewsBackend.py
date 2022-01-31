from decimal import DivisionByZero
from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
import django.apps

from diverse.forms import *

from .models import *

# Create your views here.

# BACKEND

# class indexListView(ListView):
#    model = color
#    template_name = 'index.html'
#    content_object_name = 'indexList'

def indexList(request):
    colores = color.objects.all()
    categorias = categoria.objects.all()
    tallas = talla.objects.all()
    return render(request, 'diverseBackend/index.html', {'colores': colores, 'categorias':categorias, 'tallas': tallas})

@login_required(login_url='backendLogin')
def crearColor(request):
    if request.method == 'POST':
        form = colorForm(request.POST)
        if form.is_valid():
            colorDatosForm = form.cleaned_data

            colorDatos = color(
                nombre = colorDatosForm['nombreColor'],
            )

            colorDatos.save()
        return redirect('indexBackend')
    else:
        form = colorForm()
    
    return render(request, 'diverseBackend/color_form.html', {'form':form})

@login_required(login_url='backendLogin')
def crearCategoria(request):
    if request.method == 'POST':
        form = categoriaForm(request.POST)
        if form.is_valid():
            categoriaDatosForm = form.cleaned_data

            categoriaDatos = categoria(
                tipo = categoriaDatosForm['nombreCategoria'],
            )

            categoriaDatos.save()
        return redirect('indexBackend')
    else:
        form = categoriaForm()
    
    return render(request, 'diverseBackend/categoria_form.html', {'form':form})

@login_required(login_url='backendLogin')
def crearTalla(request):
    if request.method == 'POST':
        form = tallaForm(request.POST)
        if form.is_valid():
            tallaDatosForm = form.cleaned_data

            tallaDatos = talla(
                nombre = tallaDatosForm['nombreTalla'],
            )

            tallaDatos.save()
        return redirect('indexBackend')
    else:
        form = tallaForm()
    
    return render(request, 'diverseBackend/talla_form.html', {'form':form})