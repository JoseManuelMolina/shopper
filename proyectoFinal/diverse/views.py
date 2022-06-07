from importlib.metadata import metadata
from itertools import product
from sys import flags
from urllib import request
from datetime import date

import stripe, re

from django.http import JsonResponse, HttpResponse
from django.http.response import HttpResponseRedirect

from django.urls import reverse

from django.shortcuts import redirect, render
from django.conf import settings
from django.core.paginator import Paginator
from django.core.mail import send_mail

from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, TemplateView, DeleteView
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from diverse.models import *
from account.models import *
from diverse.forms import *

from django.urls import reverse_lazy

stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

# Create your views here.

# FRONTEND

class SuccessView(TemplateView):
    template_name = 'diverse/success.html'

class CancelView(TemplateView):
    template_name = 'diverse/cancel.html'

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
    template_name = 'diverse/editarDirecciones.html'
    success_url = reverse_lazy('direcciones')

class verPedidos(LoginRequiredMixin, ListView):
    model = pedido
    context_object_name = 'pedidos'
    template_name = 'diverse/pedidos.html'

    def get_queryset(self):
        return super().get_queryset().filter(cliente_id=self.request.user.id, estado=1)

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

class editarCarrito(LoginRequiredMixin, TemplateView):
    template_name = 'diverse/carrito.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)

class borrarProductoCarrito(LoginRequiredMixin, TemplateView):
    template_name = 'diverse/carrito.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs.get('pk')
        productoCarrito_obj = productoCarrito.objects.get(id = pk)
        carrito_obj = carrito.objects.get(id = productoCarrito_obj.carrito_id)

        print(carrito_obj.precio)
        carrito_obj.precio = carrito_obj.precio - productoCarrito_obj.precioTotal
        print(carrito_obj.precio)
        if (carrito_obj.precio < 60):
            carrito_obj.gastosEnvio = 10
        
        if(carrito_obj.precio == 0):
            carrito_obj.precioTotal = 0
        else:
            carrito_obj.precioTotal = carrito_obj.precio + carrito_obj.gastosEnvio
        
        carrito_obj.save()
        productoCarrito_obj.delete()

        context['carrito'] = carrito_obj

        #return HttpResponseRedirect(reverse('verCarrito', args={ carrito_obj.id, }))
        return context

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

# new
@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLIC_KEY}
        return JsonResponse(stripe_config, safe=False)

class vistaCheckout(TemplateView):
    template_name = 'diverse/checkout.html'

    def get_context_data(self, **kwargs):
        direcciones_obj = direccion.objects.filter(usuario_id = self.request.user.id)
        carrito_obj = carrito.objects.get(id = self.kwargs['pk'])
        context = super(vistaCheckout, self).get_context_data(**kwargs)
        context.update({
            'direcciones': direcciones_obj,
            'carrito': carrito_obj,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
        })
        return context

@csrf_exempt
def crear_checkout_session(request, pk):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        
        carrito_id = pk
        carrito_obj = carrito.objects.get(id=carrito_id)
        productos_carrito = productoCarrito.objects.filter(carrito_id=carrito_id)

        line_items_list = []
        metadata_list = {'carritoID':carrito_id}
        metadata_list['cliente_id']=carrito_obj.cliente_id
        for producto_obj in productos_carrito:
            line_items_list.append({'name': producto_obj.producto.marca.nombre+' '+producto_obj.producto.modelo.nombre,'quantity': producto_obj.cantidad, 'currency': 'eur','amount': producto_obj.precio*100}),
            metadata_list['producto_numref_'+str(producto_obj.producto.num_ref)]=producto_obj.producto.num_ref
        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see https://stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param

            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancel/',
                customer_email = request.user.email,
                payment_method_types=['card'],
                mode='payment',
                line_items = line_items_list,
                metadata = metadata_list,
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})

@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    payload = request.body.decode('utf-8')
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=500)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        carrito_id = session['metadata']['carritoID']
        cliente_id = session['metadata']['cliente_id']
        carrito_obj = carrito.objects.get(id=carrito_id)

        carrito_obj.estado = 1
        carrito_obj.save()

        pedido_obj = pedido.objects.create(cliente_id = cliente_id, carrito_id = carrito_id, total = carrito_obj.precioTotal, fecha = date.today())        

        customer_email = session['customer_email']
        productos_list = session['metadata']

        send_mail(
            subject='DIVERSE [ES] - Confirmación del pedido',
            message='Gracias por su compra. Aqui estan los detalles de su pedido',
            recipient_list=[customer_email],
            from_email='noreplyDiverseES@gmail.com',
        )
        #for producto_obj_list in productos_list:
        #    print(session['metadata'][producto_obj_list])
        # TODO: run some custom code here

    return HttpResponse(status=200)