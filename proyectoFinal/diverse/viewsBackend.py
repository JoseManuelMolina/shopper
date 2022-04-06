from mailbox import NoSuchMailboxError
import re
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from diverse.forms import *

from diverse.models import *
from account.models import *

# Create your views here.

# BACKEND

# class indexListView(ListView):
#    model = color
#    template_name = 'index.html'
#    content_object_name = 'indexList'

def indexList(request):
    colores = color.objects.all()
    sexos = sexo.objects.all()
    tallas = talla.objects.all()
    categorias = categoria.objects.all()
    return render(request, 'diverseBackend/index.html', {'colores': colores, 'sexos':sexos, 'tallas': tallas, 'categorias' : categorias})

@login_required(login_url='backendLogin')
def perfil(request):
    if request.method == 'POST':
        form = usuarioForm(request.POST, request.FILES, request.user)
        if form.is_valid():
            form.save()
            return redirect('backendPerfil')
    else:
        usuario = request.user
        form = usuarioForm(usuario)
    
    return render(request, 'diverseBackend/perfil.html', {'form':form, 'usuario':usuario})

#----------------------------------------------------------------------------- Crear -----------------------------------------------------------------------------

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
        return redirect('verColor')
    else:
        form = colorForm()
    
    return render(request, 'diverseBackend/color_form.html', {'form':form})

@login_required(login_url='backendLogin')
def crearSexo(request):
    if request.method == 'POST':
        form = sexoForm(request.POST)
        if form.is_valid():
            sexoDatosForm = form.cleaned_data

            sexoDatos = sexo(
                tipo = sexoDatosForm['tipo'],
            )

            sexoDatos.save()
        return redirect('ver_sexo')
    else:
        form = sexoForm()
    
    return render(request, 'diverseBackend/sexo_form.html', {'form':form})

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
        return redirect('ver_talla')
    else:
        form = tallaForm()
    
    return render(request, 'diverseBackend/talla_form.html', {'form':form})

@login_required(login_url='backendLogin')
def crearCategoria(request):
    if request.method == 'POST':
        form = categoriaForm(request.POST)
        print(form)
        print(form.is_valid())
        if form.is_valid():
            
            categoriaDatosForm = form.cleaned_data

            categoriaDatos = categoria(
                nombre = categoriaDatosForm['nombreCategoria']
            )
            
            categoriaDatos.save()
        print('me voys')
        return redirect('verCategoria')
    else:
        form = categoriaForm()

    return render(request, 'diverseBackend/categoria_form.html', {'form':form})

@login_required(login_url='backendLogin')
def crearSubCategoria(request):
    if request.method == 'POST':
        form = subcategoriaForm(request.POST)
        if form.is_valid():
            subcategoriaDatosForm = form.cleaned_data

            subcategoriaDatos = subCategoria(
                nombre = subcategoriaDatosForm['nombreSubcategoria'],
                categoria_id = subcategoriaDatosForm['categoria_id']
            )

            subcategoriaDatos.save()
        return redirect('ver_subcategoria')
    else:
        form = subcategoriaForm()

    return render(request, 'diverseBackend/subcategoria_form.html', {'form' : form})

@login_required(login_url='backendLogin')
def crearMarca(request):
    if request.method == 'POST':
        form = marcaForm(request.POST)
        if form.is_valid():
            marcaDatosForm = form.cleaned_data

            marcaDatos = marca(
                nombre = marcaDatosForm['nombreMarca'],
                subCategoria_id = marcaDatosForm['subCategoria_id']
            )

            marcaDatos.save()
        return redirect('verMarca')
    else:
        form = marcaForm()

    return render(request, 'diverseBackend/marca_form.html', {'form' : form})

@login_required(login_url='backendLgin')
def crearProducto(request):

    return render(request, 'diverseBackend/producto_form.html')


#----------------------------------------------------------------------------- Ver -----------------------------------------------------------------------------
def verColor(request):
    colores = color.objects.all()
    return render(request, 'diverseBackend/ver_color.html', {'colores' : colores})

def verSexo(request):
    sexos = sexo.objects.all()
    return render(request, 'diverseBackend/ver_sexo.html', {'sexos' : sexos})

def verCategoria(request):
    categorias = categoria.objects.all()
    return render(request, 'diverseBackend/ver_categoria.html', {'categorias' : categorias})

def verSubCategoria(request):
    subCategorias = subCategoria.objects.all()
    return render(request, 'diverseBackend/ver_subcategoria.html', {'subCategorias' : subCategorias})

def verTalla(request):
    tallas = talla.objects.all()
    return render(request, 'diverseBackend/ver_talla.html', {'tallas' : tallas})

def verMarca(request):
    marcas = marca.objects.all()
    return render(request, 'diverseBackend/ver_marca.html', {'marcas' : marcas})