from email import message
from itertools import product
from sys import flags
from urllib import request
from datetime import date

import stripe, re

from django.http import JsonResponse, HttpResponse
from django.http.response import HttpResponseRedirect

from django.urls import reverse

from django.shortcuts import redirect, render
from django.template import RequestContext
from django.conf import settings
from django.core.paginator import Paginator
from django.core.mail import send_mail, EmailMessage

from django.views import View
from django.views.generic import ListView, UpdateView, TemplateView
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import update_session_auth_hash, authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
<<<<<<< HEAD

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str,force_text,DjangoUnicodeDecodeError
from .utils import generate_token
=======
>>>>>>> 64c6ce642363f36d855e5e198d72a4d594b2d7a9

from diverse.models import *
from account.models import *
from diverse.forms import *
from django.contrib.auth.models import User

from django.db.models import Q

from django.urls import reverse_lazy

stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

# Create your views here.

# FRONTEND

def enviar_correo_activacion(user, request):
    current_site = get_current_site(request)
    email_subject = 'Activa tu cuenta en DIVERSE [ES]'
    email_body = render_to_string('diverse/activar.html', {
        'usuario': user.username,
        'dominio': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user),
    })

    email = EmailMessage(subject=email_subject,body=email_body,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to=[user.email]
                        )

    email.send()

class SuccessView(TemplateView):
    template_name = 'diverse/success.html'

class CancelView(TemplateView):
    template_name = 'diverse/cancel.html'

def page_not_found_view(request, exception):
    return render(request, 'diverse/404.html', status=404)

def login_user(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST.get('loginEmail', False)
        password = request.POST.get('loginPassword', False)

        user = authenticate(email=username, password=password)
        print(user)
        if user is not None:
            if user.is_email_verificado:
                login(request, user)
                return HttpResponseRedirect('perfil')
            else:
                messages.add_message(request, messages.ERROR, 'Debe verificar su cuenta para poder loguearse')
    return render(request, 'diverse/login.html', {'request': RequestContext(request)})

def registarUsuario(request):
    errorContraseña = ''
    if request.method == 'POST':
        form = registrarUsuarioForm(request.POST)

        print(form.errors)
        if form.is_valid():
            
            usuarioDatosForm = form.cleaned_data
            confirmarContraseña = request.POST.get('confirmarContraseña' , False)

            if(usuarioDatosForm['password']==confirmarContraseña):
            
                contraseñaEncriptada=make_password(usuarioDatosForm['password'])
                
                usuarioDatos = Account(
                    nombre = usuarioDatosForm['nombre'],
                    apellidos = usuarioDatosForm['apellidos'],
                    username = usuarioDatosForm['username'],
                    email = usuarioDatosForm['email'],
                    telefono = usuarioDatosForm['telefono'],
                    password = contraseñaEncriptada,
                    is_email_verificado = False,
                )

                usuarioDatos.save()
                enviar_correo_activacion(usuarioDatos, request)

                messages.add_message(request, messages.SUCCESS, '!Cuenta creada! Le hemos enviado un email de verificación, debe verificar su cuenta para loguearse')

                return redirect('login')

            errorContraseña = 'Error'

        return render(request, 'diverse/registro.html', {'form' : form, 'errorContraseña': errorContraseña})
    else:
        form = registrarUsuarioForm()

    return render(request, 'diverse/registro.html', {'form' : form, 'errorContraseña': errorContraseña})


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

class filtros(TemplateView):
    template_name = 'diverse/filter.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            col = self.request.GET.get('color')
            color_obj = color.objects.filter(id = col)
        except:
            col = -1
            color_obj = color.objects.all()
        try:
            sc = self.request.GET.get('sc')       
        except:
            sc = -1
        print("----------------------------------------")    
        print('sc', sc) 

        if sc != -1:
            sc_obj = subCategoria.objects.filter(id = sc)
        else:
            sc_obj = subCategoria.objects.all()

        try:
            tall = request.GET('talla')
            talla_obj = talla.objects.filter(id = tall)
        except:
            tall = -1
            tall_obj = talla.objects.all()
        print("----------------------------------------")    
        print('talla', tall)

        if tall != -1:
            tall_obj = talla.objects.filter(id = sc)
        else:
            tall_obj = talla.objects.all()

        try:
            mc = request.GET('marca')
            print('mc', mc)
            marca_obj = marca.objects.filter(id = mc)
        except:
            mc = -1
            marca_obj = marca.objects.all()

        productos = ''

        context ={
            "color" : color_obj,
            "subcategoria" : sc_obj,
            "talla" : tall_obj,
            "marca" : marca_obj,
            'productos' : productos
        }

        print(context)

        return context

def index(request):

    lista_nav = funcionNav()

    context = {
        "lista_nav" : lista_nav,
        "productos" : producto.objects.all().distinct('modelo_id')

    }
    return render(request, 'diverse/index.html', context)

@login_required(login_url='login')
def perfil(request):
    usuario = request.user
    contraseñaAntigua = usuario.password
    form = infoPersonal(instance=usuario)
    lista_nav = funcionNav()

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
    
    return render(request, 'diverse/perfil.html', {'form':form, 'usuario':request.user, "lista_nav" : lista_nav})

class direcciones(LoginRequiredMixin, ListView):
    model = direccion
    context_object_name = 'direcciones'
    template_name = 'diverse/direcciones.html'

    def get_context_data(self, **kwargs):
        context = super(direcciones,self).get_context_data(**kwargs)
        context['direcciones'] = direccion.objects.filter(usuario_id=self.request.user.id)
        context['lista_nav'] = funcionNav()

        return context

    def get_queryset(self):
        return super().get_queryset().filter(usuario_id=self.request.user.id)

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

    return render(request, 'diverse/crearDireccion.html', {'form' : form, "lista_nav" : funcionNav()})

class editarDireccion(LoginRequiredMixin, UpdateView):
    model = direccion
    fields = '__all__'
    exclude = ['usuario', ]
    template_name = 'diverse/editarDirecciones.html'
    success_url = reverse_lazy('direcciones')

    def get_context_data(self, **kwargs):
        context = super(editarDireccion,self).get_context_data(**kwargs)
        context['lista_nav'] = funcionNav()
        return context

class verPedidos(LoginRequiredMixin, TemplateView):
    template_name = 'diverse/pedidos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pedidos_obj = pedido.objects.filter(cliente_id=self.request.user.id)

        paginator = Paginator(pedidos_obj, 3)

        page_number = self.request.GET.get('page')
        pedidos_pagina = paginator.get_page(page_number)

        context['pedidos']=pedidos_obj
        context['pedidos_lista']=pedidos_pagina

        return context

class verPedido(LoginRequiredMixin, TemplateView):
    template_name = 'diverse/pedido.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pedido_id = self.kwargs['pk']
        pedido_obj = pedido.objects.get(id=pedido_id, cliente_id=self.request.user.id)

        context['pedido']=pedido_obj

        return context

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
        context['lista_nav'] = funcionNav()

        return context

class añadirCarrito(LoginRequiredMixin, TemplateView):
    template_name = 'diverse/carrito.html'

    #def get_context_data(self, **kwargs):
    def dispatch(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        # obtiene el numRef del producto por la requested url
        producto_numRef = self.kwargs['pk']
        # obtener el producto
        producto_obj = producto.objects.get(num_ref=producto_numRef)
        # obtiene los carritos del cliente
        carritos_usuario = carrito.objects.filter(cliente_id = self.request.user.id)

        try:
            st_producto = stock.objects.get(num_ref_producto_id = producto_numRef)
            messages.error(request, 'Producto fuera de stock')
        except:
            return redirect('verCarrito')

        if stock.objects.get(num_ref_producto_id = producto_numRef).cantidad <= 0:
            messages.error(request, 'Producto fuera de stock')
            return redirect('verCarrito')

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
                    if stock.objects.get(num_ref_producto_id = producto_numRef).cantidad < productocarrito.cantidad+1:
                        messages.error(request, 'Producto fuera de stock')
                        return redirect('verCarrito')
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
        context['lista_nav'] = funcionNav()

        return redirect('verCarrito')

class editarCarrito(LoginRequiredMixin, TemplateView):
    template_name = 'diverse/carrito.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lista_nav'] = funcionNav()

        #print(context)

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
        context['lista_nav'] = funcionNav()

        #return HttpResponseRedirect(reverse('verCarrito', args={ carrito_obj.id, }))
        return context

def catalogoH(request):

    marcas = marca.objects.all()
    colores = color.objects.all()
    tallas = talla.objects.all()
    categorias = categoria.objects.all()
    subcategorias = subCategoria.objects.all()
    #productos = producto.objects.filter(sexo=1)

    try:
        order = request.GET['order']
    except:
        order = -1
    print(order)
    if order == -1:
        productos = list(producto.objects.filter(sexo=1))
    elif order == 0:
        productos = list(producto.objects.filter(sexo=1).order_by('precio'))
    else:
        productos = list(producto.objects.filter(sexo=1).order_by('-precio'))

    #print(productos)

    #filtros(request)        
    
    paginator = Paginator(productos, 5)

    page_number = request.GET.get('page')
    productos_pagina = paginator.get_page(page_number)

    
    lista_nav = funcionNav()

    context = {
        "sexo_obj" : 'h',
        'sexo' : 'Hombre',
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
    stock_obj = stock.objects.filter(num_ref_producto_id = pk)

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

    lista_nav = funcionNav()

    context = {
        'producto' : productoSimple,
        'imagenesextra' : imagenesExtra,
        'productoscolor' : productosColor,
        'productostalla' : productosTalla,
        'productosrelacionados' : productosRelacionados,
        'lista_nav' : lista_nav,
        'stock' : stock_obj,
    }

    return render(request, 'diverse/producto_list.html', context)

# new
@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLIC_KEY}
        return JsonResponse(stripe_config, safe=False)

class vistaCheckout(LoginRequiredMixin, TemplateView):
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
        line_items_list.append({'name': 'Gastos Envío','currency': 'eur','quantity': 1, 'amount': carrito_obj.gastosEnvio*100}),
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
            print(checkout_session)
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
        productoCarrito_obj = productoCarrito.objects.filter(carrito_id=carrito_id)

        carrito_obj.estado = 1
        carrito_obj.save()

        for producto_obj in productoCarrito_obj:
            stockProducto_obj = stock.objects.get(num_ref_producto_id=producto_obj.producto_id)
            stockProducto_obj.cantidad = stockProducto_obj.cantidad-producto_obj.cantidad
            stockProducto_obj.save()

        pedido_obj = pedido.objects.create(cliente_id = cliente_id, carrito_id = carrito_id, total = carrito_obj.precioTotal, fecha_pedido = date.today())        

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

def activate_user(request, uidb64, token):
    try:
        uid=force_text(urlsafe_base64_decode(uidb64))

        user=Account.objects.get(pk=uid)

    except Exception as e:
        user = None

    if user and generate_token.check_token(user,token):
        user.is_email_verificado=True
        user.save()

        messages.add_message(request, messages.SUCCESS, 'Email verificado correctamente')
        return redirect(reverse('login'))

    return render(request,'diverse/error-activacion.html',{'user':user})