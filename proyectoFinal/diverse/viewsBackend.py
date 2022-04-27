from mailbox import NoSuchMailboxError
import re
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from diverse.forms import *

from diverse.models import *
from account.models import *

from django.http import JsonResponse

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
        return redirect('verSexo')
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
        return redirect('verTalla')
    else:
        form = tallaForm()
    
    return render(request, 'diverseBackend/talla_form.html', {'form':form})

@login_required(login_url='backendLogin')
def crearCategoria(request):
    if request.method == 'POST':
        form = categoriaForm(request.POST)
        if form.is_valid():

            form.save()

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
                nombre = subcategoriaDatosForm['nombre'],
                categoria_id = subcategoriaDatosForm['categoria_id']
            )

            subcategoriaDatos.save()
        return redirect('verSubCategoria')
    else:
        form = subcategoriaForm()

    return render(request, 'diverseBackend/subcategoria_form.html', {'form' : form})

@login_required(login_url='backendLogin')
def crearMarca(request):
    if request.method == 'POST':
        form = marcaForm(request.POST)
        if form.is_valid():
            
            form.save()
            
        return redirect('verMarca')
    else:
        form = marcaForm()

    return render(request, 'diverseBackend/marca_form.html', {'form' : form})

@login_required(login_url='backendLogin')
def crearModelo(request):
    if request.method == 'POST':
        form = modeloForm(request.POST)
        if form.is_valid():
            
            modeloDatosForm = form.cleaned_data

            modeloDatos = modelo(
                nombre = modeloDatosForm['nombre'],
                marca_id = modeloDatosForm['marca_id']
            )

            modeloDatos.save()
            
        return redirect('verModelo')
    else:
        form = modeloForm()

    return render(request, 'diverseBackend/modelo_form.html', {'form' : form})

@login_required(login_url='backendLogin')
def crearProducto(request):
    if request.method == 'POST':
        form = productoForm(request.POST)
        if form.is_valid():
            
            productoDatosForm = form.cleaned_data

            productoDatos = modelo(
                num_ref = productoDatosForm['num_ref'],
                precio = productoDatosForm['precio'],
                imagen = productoDatosForm['iamgen'],
                marca_id = productoDatosForm['marca_id']
            )

            productoDatos.save()
            
        return redirect('verProducto')
    else:
        form = productoForm()

    return render(request, 'diverseBackend/producto_form.html', {'form' : form})


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

def verModelo(request):
    modelos = modelo.objects.all()

    return render(request, 'diverseBackend/ver_modelo.html', {'modelos' : modelos})

def verProducto(request):
    productos = producto.objects.all()
    return render(request, 'diverseBackend/ver_producto.html', {'productos' : productos})


#--------------------------------------------------------------------- Obtener modelos ------------------------------------------------------------------------------
def obtenerModelos(request):
    marcaForm = request.POST.get('marca')
    marcaForm = marca.objects.filter(id=marcaForm)
    modelos = list(modelo.objects.filter(marca_id=marcaForm).values('id', 'nombre'))
    response_data = {
        "modelos":modelos
    }

    return JsonResponse(response_data)

# AJAX
def load_modelos(request):
    marca_id_form = request.GET.get('marca_id')
    modelos = modelo.objects.filter(marca_id = marca_id_form)

    return render(request, 'diverseBackend/modelos_dropdown_list_options.html', {'modelos' : modelos})