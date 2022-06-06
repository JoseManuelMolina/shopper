from itertools import product
from sys import flags
from django.shortcuts import redirect, render
from django.core.paginator import Paginator

from django.views.generic import ListView, CreateView, UpdateView, TemplateView
from django.views.generic.base import View

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

def funcionNav():
    categoriasHId = producto.objects.filter(sexo_id=1).values_list("categoria_id", flat=True).distinct()
    categoriasH = []
    categoriasMId = producto.objects.filter(sexo_id=2).values_list("categoria_id", flat=True).distinct()
    categoriasM = []
    categoriasNoId = producto.objects.filter(sexo_id=3).values_list("categoria_id", flat=True).distinct()
    categoriasNo = []
    categoriasNaId = producto.objects.filter(sexo_id=4).values_list("categoria_id", flat=True).distinct()
    categoriasNa = []

    marcasHId = producto.objects.filter(sexo_id=1).values_list("marca_id", flat=True).distinct()
    marcasH = []
    marcasMId = producto.objects.filter(sexo_id=2).values_list("marca_id", flat=True).distinct()
    marcasM = []
    marcasNoId = producto.objects.filter(sexo_id=3).values_list("marca_id", flat=True).distinct()
    marcasNo = []
    marcasNaId = producto.objects.filter(sexo_id=4).values_list("marca_id", flat=True).distinct()
    marcasNa = []

    for i in marcasHId:
        marcasH.append(marca.objects.get(id=i))

    for j in marcasMId:
        marcasM.append(marca.objects.get(id=j))

    for u in marcasNoId:
        marcasNo.append(marca.objects.get(id=u))

    for r in marcasNaId:
        marcasNa.append(marca.objects.get(id=r))

    for w in categoriasNaId:
        categoriasNa.append(categoria.objects.get(id=w))

    for v in categoriasNoId:
        categoriasNo.append(categoria.objects.get(id=v))
    
    for y in categoriasHId:
        categoriasH.append(categoria.objects.get(id=y))

    for x in categoriasMId:
        categoriasM.append(categoria.objects.get(id=x))

    contenido = {
        'categoriasM' : categoriasM,
        'categoriasH' : categoriasH,
        'categoriasNo' : categoriasNo,
        'categoriasNa' : categoriasNa,
        'marcasH' : marcasH,
        'marcasM' : marcasM,
        'marcasNo' : marcasNo,
        'marcasNa' : marcasNa,
    }

    return contenido

def index(request):

    lista_nav = funcionNav()

    context = {
        "lista_nav" : lista_nav

    }
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

class verCarrito(LoginRequiredMixin, TemplateView):
    template_name = 'diverse/carrito.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        carritos_usuario = carrito.objects.filter(cliente_id = self.request.user.id)
        if carritos_usuario.count() > 0:
            ultimoCarrito = carritos_usuario[carritos_usuario.count()-1]
            if ultimoCarrito.estado == 0:
                carrito_obj = carrito.objects.get(id = ultimoCarrito.id)
            else:
                carrito_obj = None
        else:
            carrito_obj = None

        context['carrito'] = carrito_obj

        return context

class añadirCarrito(LoginRequiredMixin, TemplateView):
    template_name = 'diverse/carrito.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # obtiene el numRef del producto por la requested url
        producto_numRef = self.kwargs['pk']
        # obtener el producto
        producto_obj = producto.objects.get(num_ref=producto_numRef)
        # obtiene los carritos del cliente
        carritos_usuario = carrito.objects.filter(cliente_id = self.request.user.id)

        # chequea si el usuario tiene algun carrito
        if carritos_usuario.count() > 0:
            # obtiene el ultimo carrito existente del cliente
            ultimoCarrito = carritos_usuario[carritos_usuario.count()-1]

            # comprueba si el ultimo carrito esta en proceso de compra o ya esta comprado
            if ultimoCarrito.estado == 0:
                carrito_obj = carrito.objects.get(id=ultimoCarrito.id)
                producto_en_carrito = carrito_obj.productocarrito_set.filter(producto=producto_obj)
                
                # producto ya existente en el carrito
                if producto_en_carrito.exists():
                    productocarrito = producto_en_carrito.last()
                    productocarrito.cantidad += 1
                    productocarrito.precioTotal += producto_obj.precio
                    productocarrito.save()
                    carrito_obj.precio += producto_obj.precio
                    if carrito_obj.precio > 60:
                        carrito_obj.gastosEnvio = 0
                    carrito_obj.precioTotal = carrito_obj.precio + carrito_obj.gastosEnvio
                    carrito_obj.save()

                # nuevo producto añadido en el carrito
                else:
                    productocarrito = productoCarrito.objects.create(carrito_id = carrito_obj.id, producto_id = producto_obj.num_ref, precio = producto_obj.precio, cantidad = 1, precioTotal = producto_obj.precio)
                    carrito_obj.precio += producto_obj.precio
                    if carrito_obj.precio > 60:
                        carrito_obj.gastosEnvio = 0
                    carrito_obj.precioTotal = carrito_obj.precio + carrito_obj.gastosEnvio
                    carrito_obj.save()

            # si esta comprado, crea un carrito nuevo
            else:
                carrito_obj = carrito.objects.create(precio=0, cliente_id=self.request.user.id, estado = 0)
                self.request.session['carrito_id'] = carrito_obj.id
                productocarrito = productoCarrito.objects.create(carrito_id = carrito_obj.id, producto_id = producto_obj.num_ref, precio = producto_obj.precio, cantidad = 1, precioTotal = producto_obj.precio)
                carrito_obj.precio += producto_obj.precio
                if carrito_obj.precio > 60:
                    carrito_obj.gastosEnvio = 0
                carrito_obj.precioTotal = carrito_obj.precio + carrito_obj.gastosEnvio
                carrito_obj.save()

        # si no tiene carritos lo crea
        else:
            carrito_obj = carrito.objects.create(precio=0, cliente_id=self.request.user.id, estado = 0)
            self.request.session['carrito_id'] = carrito_obj.id
            productocarrito = productoCarrito.objects.create(carrito_id = carrito_obj.id, producto_id = producto_obj.num_ref, precio = producto_obj.precio, cantidad = 1, precioTotal = producto_obj.precio)
            carrito_obj.precio += producto_obj.precio
            if carrito_obj.precio > 60:
                carrito_obj.gastosEnvio = 0
            carrito_obj.precioTotal = carrito_obj.precio + carrito_obj.gastosEnvio
            carrito_obj.save()
    
        context['carrito'] = carrito_obj

        return context

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

    
    lista_nav = funcionNav()

    context = {
        "sexo" : "hombre",
        #"productos" : productosH,
        "productos" : productos_pagina,
        "marcas" : marcas,
        "colores" : colores,
        "tallas" : tallas,
        "categorias" : categorias,
        "subcategorias" : subcategorias,
        "lista_nav" : lista_nav,
    }

    print(context)



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

    lista_nav = funcionNav()


    context = {
        "sexo" : "mujer",
        #"productos" : productosH,
        "productos" : productos_pagina,
        "marcas" : marcas,
        "colores" : colores,
        "tallas" : tallas,
        "categorias" : categorias,
        "subcategorias" : subcategorias,
        "lista_nav" : lista_nav,

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

    lista_nav = funcionNav()


    context = {
        "sexo" : "niño",
        #"productos" : productosH,
        "productos" : productos_pagina,
        "marcas" : marcas,
        "colores" : colores,
        "tallas" : tallas,
        "categorias" : categorias,
        "subcategorias" : subcategorias,
        "lista_nav" : lista_nav,

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

    lista_nav = funcionNav()


    context = {
        "sexo" : "niña",
        #"productos" : productosH,
        "productos" : productos_pagina,
        "marcas" : marcas,
        "colores" : colores,
        "tallas" : tallas,
        "categorias" : categorias,
        "subcategorias" : subcategorias,
        "lista_nav" : lista_nav,

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

    productosRelacionados = producto.objects.filter(sexo_id = productoSimpleDatos.sexo_id)[:4]

    context = {
        'producto' : productoSimple,
        'imagenesextra' : imagenesExtra,
        'productoscolor' : productosColor,
        'productostalla' : productosTalla,
        'productosrelacionados' : productosRelacionados,
    }

    return render(request, 'diverse/producto_list.html', context)