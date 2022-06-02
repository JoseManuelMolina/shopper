from audioop import reverse
from math import prod
from pyexpat import model
import re
from django.shortcuts import redirect, render

from django.views.generic import ListView, CreateView, UpdateView, TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from diverse.models import *
from account.models import *
from diverse.forms import *

from mailbox import NoSuchMailboxError
from re import template
from sre_constants import SUCCESS
from django.urls import reverse_lazy

from django.http import HttpResponseRedirect, JsonResponse

# Create your views here.

# class indexListView(ListView):WWW
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
    usuario = request.user
    formUsuario = usuarioForm(instance=usuario)
    formImagenUsuario = imagenUsuario(instance=usuario)

    if request.method == 'POST':
        formUsuario = usuarioForm(request.POST, instance=usuario)
        formImagenUsuario = imagenUsuario(request.POST, request.FILES, instance=usuario)

        if formUsuario.is_valid() and formImagenUsuario.is_valid():
            print(formImagenUsuario)
            formUsuario.save()
            formImagenUsuario.save()
            return redirect('backendPerfil')

    else:
        formUsuario = usuarioForm(instance=request.user)
        formImagenUsuario = imagenUsuario(instance=request.user)
    
    return render(request, 'diverseBackend/perfil.html', {'form':formUsuario, 'formImagen':formImagenUsuario, 'usuario':request.user})

#----------------------------------------------------------------------------- CREAR -----------------------------------------------------------------------------

@login_required(login_url='backendLogin')
def crearColor(request):
    if request.method == 'POST':
        form = colorForm(request.POST)
        if form.is_valid():

            form.save()
            
        return redirect('verColor')
    else:
        form = colorForm()
    
    return render(request, 'diverseBackend/color_form.html', {'form':form})

@login_required(login_url='backendLogin')
def crearSexo(request):
    if request.method == 'POST':
        form = sexoForm(request.POST)
        if form.is_valid():

            form.save()
            
        return redirect('verSexo')
    else:
        form = sexoForm()
    
    return render(request, 'diverseBackend/sexo_form.html', {'form':form})

@login_required(login_url='backendLogin')
def crearTalla(request):
    if request.method == 'POST':
        form = tallaForm(request.POST)
        if form.is_valid():

            form.save()

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


class crearProducto(LoginRequiredMixin, CreateView):

    model = producto
    form_class = productoForm
    template_name = 'diverseBackend/producto_form.html'
    success_url = reverse_lazy('verProducto')

    def form_valid(self, form):
        #print(form)
        #return 
        form.save()
        return super(crearProducto, self).form_valid(form)
        

#----------------------------------------------------------------------------- VER -----------------------------------------------------------------------------
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

class verProducto(ListView):
    model = producto
    context_object_name = 'productos'
    template_name = 'diverseBackend/ver_producto.html'

def verProductoSimple(request, pk):
    productoSimple = producto.objects.filter(num_ref = pk)
    imagenesExtra = imagenProducto.objects.filter(producto_numref_id = pk)
    context = {
        'producto' : productoSimple,
        'imagenes' : imagenesExtra,
    }
    

    return render(request, 'diverseBackend/producto.html', context)

#----------------------------------------------------------------------------- EDITAR -----------------------------------------------------------------------------
class editarColor(LoginRequiredMixin, UpdateView):
    model = color
    fields = '__all__'
    template_name = 'diverseBackend/modelo_form.html'
    success_url = reverse_lazy('verColor')

class editarCategoria(LoginRequiredMixin, UpdateView):
    model = categoria
    fields = '__all__'
    template_name = 'diverseBackend/categoria_form.html'
    success_url = reverse_lazy('verCategoria')

class editarSubCategoria(LoginRequiredMixin, UpdateView):
    model = subCategoria
    fields = '__all__'
    template_name = 'diverseBackend/subCategoria_form.html'
    success_url = reverse_lazy('verSubCategoria')

class editarTalla(LoginRequiredMixin, UpdateView):
    model = talla
    fields = '__all__'
    template_name = 'diverseBackend/talla_form.html'
    success_url = reverse_lazy('verTalla')

class editarMarca(LoginRequiredMixin, UpdateView):
    model = marca
    fields = '__all__'
    template_name = 'diverseBackend/marca_form.html'
    success_url = reverse_lazy('verMarca')

class editarModelo(LoginRequiredMixin, UpdateView):
    model = modelo
    fields = '__all__'
    template_name = 'diverseBackend/modelo_form.html'
    success_url = reverse_lazy('verModelo')

class editarProducto(LoginRequiredMixin, UpdateView):
    model = producto
    fields = '__all__'
    template_name = 'diverseBackend/producto_form.html'
    success_url = reverse_lazy('verProducto')

    def form_valid(self, form, **kwargs):
        pk = self.kwargs.get('pk')
        numRef_nuevo = producto.objects.filter(num_ref = form['num_ref'].value())

        if numRef_nuevo.count() == 0:
            producto_obj = producto.objects.get(num_ref = pk)
            producto_obj.delete()

        return super(editarProducto, self).form_valid(form)        

@login_required
def eliminarProducto(request, pk):
    product = producto.objects.filter(num_ref = pk)
    product.delete()
    
    return redirect('verProducto')

@login_required  
def agregarFotos(request, primarykey):
    if request.method == 'POST':
        form = imagenProductoForm(request.POST, request.FILES)
        
        if form.is_valid():

            imagenDatosForm = form.cleaned_data

            print(imagenDatosForm)
            imagenDatos = imagenProducto(
                imagen = imagenDatosForm['imagen'],
                producto_numref_id = primarykey
            ) 

            print(request.FILES)

            imagenDatos.save()
            
        return redirect('verProductoSimple', pk=primarykey)
        
        
    else:
        form = imagenProductoForm()
        

    return render(request, 'diverseBackend/imagenProducto.html', {'form' : form})

@login_required
def eliminarFoto(request, pkproducto ,pkfoto):
    imagen = imagenProducto.objects.filter(id=pkfoto)
    product = producto.objects.filter(num_ref = pkproducto)
    imagen.delete()
    
    return redirect('verProductoSimple', pk=pkproducto)

#--------------------------------------------------------------------- Obtener modelos ------------------------------------------------------------------------------
# AJAX
def load_modelos(request):
    marca_id_form = request.GET.get('marca_id')
    modelos = modelo.objects.filter(marca_id = marca_id_form)

    return render(request, 'diverseBackend/modelos_dropdown_list_options.html', {'modelos' : modelos})

def load_subcategorias(request):
    categoria_id_form = request.GET.get('categoria_id')
    subcategorias = subCategoria.objects.filter(categoria_id = categoria_id_form)

    return render(request, 'diverseBackend/subcategorias_dropdown_list_options.html', {'subcategorias' : subcategorias})