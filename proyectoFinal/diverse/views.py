from itertools import product
from django.shortcuts import redirect, render
from django.core.paginator import Paginator

from django.views.generic import ListView, CreateView, UpdateView, TemplateView
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import make_password, check_password
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
    contraseñaAntigua = usuario.password
    form = infoPersonal(instance=usuario)

    if request.method == 'POST':
        form = infoPersonal(request.POST, instance=usuario)

        if form.is_valid():

            if(request.POST['password'] == usuario.password):
                contraseñaEncriptada=make_password(request.POST['password'])
                usuario.password = contraseñaEncriptada
                update_session_auth_hash(request, request.user)
                
            form.save()

            if(contraseñaAntigua != usuario.password):
                update_session_auth_hash(request, request.user)

            return redirect('perfil')

    else:
        form = infoPersonal(instance=request.user)
    
    return render(request, 'diverse/perfil.html', {'form':form, 'usuario':request.user})

class direcciones(LoginRequiredMixin, ListView):
    model = direccion
    context_object_name = 'direcciones'
    template_name = 'diverse/direcciones.html'

    def get_queryset(self):
        return super().get_queryset().filter(usuario=self.request.user.id)

@login_required(login_url='login')
def crearDireccion(request):
    if request.method == 'POST':
        form = direccionesForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.usuario = request.user
            form.save()
        return redirect('direcciones')
    else:
        form = direccionesForm(initial={'usuario': request.user.id})

    return render(request, 'diverse/crearDireccion.html', {'form' : form})

class editarDireccion(LoginRequiredMixin, UpdateView):
    model = direccion
    fields = '__all__'
    exclude = ['usuario', ]
    template_name = 'diverse/crearDireccion.html'
    success_url = reverse_lazy('direcciones')


def cart(request):
    context = {}
    return render(request, 'diverse/cart.html', context)

def checkout(request):
    context = {}
    return render(request, 'diverse/checkout.html', context)

def catalogoH(request):

    marcas = marca.objects.all()
    colores = color.objects.all()
    tallas = talla.objects.all()
    categorias = categoria.objects.all()
    subcategorias = subCategoria.objects.all()
    productos = producto.objects.filter(sexo=1)
    
    paginator = Paginator(productos, 5)

    page_number = request.GET.get('page')
    productos_pagina = paginator.get_page(page_number)

    context = {
        "sexo" : "hombre",
        #"productos" : productosH,
        "productos" : productos_pagina,
        "marcas" : marcas,
        "colores" : colores,
        "tallas" : tallas,
        "categorias" : categorias,
        "subcategorias" : subcategorias,

    }


    return render(request, 'diverse/catalogo.html', context)

def catalogoM(request):
    marcas = marca.objects.all()
    colores = color.objects.all()
    tallas = talla.objects.all()
    categorias = categoria.objects.all()
    subcategorias = subCategoria.objects.all()
    productos = producto.objects.filter(sexo=2)

    paginator = Paginator(productos, 5)

    page_number = request.GET.get('page')
    productos_pagina = paginator.get_page(page_number)



    context = {
        "sexo" : "mujer",
        #"productos" : productosH,
        "productos" : productos_pagina,
        "marcas" : marcas,
        "colores" : colores,
        "tallas" : tallas,
        "categorias" : categorias,
        "subcategorias" : subcategorias,

    }

    return render(request, 'diverse/catalogo.html', context)

def catalogoNo(request):
    marcas = marca.objects.all()
    colores = color.objects.all()
    tallas = talla.objects.all()
    categorias = categoria.objects.all()
    subcategorias = subCategoria.objects.all()
    productos = producto.objects.filter(sexo=3)

    paginator = Paginator(productos, 5)

    page_number = request.GET.get('page')
    productos_pagina = paginator.get_page(page_number)

    context = {
        "sexo" : "niño",
        #"productos" : productosH,
        "productos" : productos_pagina,
        "marcas" : marcas,
        "colores" : colores,
        "tallas" : tallas,
        "categorias" : categorias,
        "subcategorias" : subcategorias,

    }
    return render(request, 'diverse/catalogo.html', context)

def catalogoNa(request):
    marcas = marca.objects.all()
    colores = color.objects.all()
    tallas = talla.objects.all()
    categorias = categoria.objects.all()
    subcategorias = subCategoria.objects.all()
    productos = producto.objects.filter(sexo=4)

    paginator = Paginator(productos, 5)

    page_number = request.GET.get('page')
    productos_pagina = paginator.get_page(page_number)

    context = {
        "sexo" : "niña",
        #"productos" : productosH,
        "productos" : productos_pagina,
        "marcas" : marcas,
        "colores" : colores,
        "tallas" : tallas,
        "categorias" : categorias,
        "subcategorias" : subcategorias,

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

class productoSingle2(ListView):
    model = producto
    #context_object_name = 'productos'
    template_name: 'diverse/producto_list_v2.html'

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return qs.filter(num_ref = self.kwargs['pk'])

def productoSingle(request, pk):
    productoSimpleDatos = producto.objects.get(num_ref = pk)
    productoSimple = producto.objects.filter(num_ref = pk)
    imagenesExtra = imagenProducto.objects.filter( producto_numref_id = pk)

    productosColor = producto.objects.filter(sexo_id = productoSimpleDatos.sexo_id, 
        categoria_id = productoSimpleDatos.categoria_id,
        subCategoria_id = productoSimpleDatos.subCategoria_id,
        marca_id = productoSimpleDatos.marca_id,
        modelo_id = productoSimpleDatos.modelo_id,
        talla_id = productoSimpleDatos.talla_id).exclude(color_id = productoSimpleDatos.color_id)

    
    productosTalla = producto.objects.filter(sexo_id = productoSimpleDatos.sexo_id, 
        categoria_id = productoSimpleDatos.categoria_id,
        subCategoria_id = productoSimpleDatos.subCategoria_id,
        marca_id = productoSimpleDatos.marca_id,
        modelo_id = productoSimpleDatos.modelo_id,
        color_id = productoSimpleDatos.color_id)

    print(productosTalla.query)


    context = {
        'producto' : productoSimple,
        'imagenesextra' : imagenesExtra,
        'productoscolor' : productosColor,
    }

    return render(request, 'diverse/producto_list.html', context)