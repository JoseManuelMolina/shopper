from unicodedata import name

from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, logout_then_login

from . import viewsBackend
from . import views

from diverse.viewsBackend import *
from diverse.views import *

from django.conf import settings


urlpatterns = [
    #Deja la cadena vacía para usar la url base (/)

    #FRONTEND
    path('', views.index, name="index"),
     path('config/', views.stripe_config),
    path('success/', SuccessView.as_view(), name="success"),
    path('cancel/', CancelView.as_view(), name="cancel"),
    path('login', views.login_user, name="login"),
    path('logout', logout_then_login,name="cerrarSesion"),
    path('registro', views.registarUsuario, name="registro"),
    path('perfil/', views.perfil, name="perfil"),
    path('perfil/direcciones', views.direcciones.as_view(), name="direcciones"),
    path('perfil/direcciones/añadir', views.crearDireccion, name="añadirDireccion"),
    path('perfil/direcciones/<int:pk>', views.editarDireccion.as_view(), name="editarDireccion"),
    path('perfil/pedidos', views.verPedidos.as_view(), name="verPedidos"),
    path('perfil/pedidos/<int:pk>', views.verPedido.as_view(), name="verPedido"),
    path('perfil/carrito', verCarrito.as_view(), name="verCarrito"),
    path('perfil/añadir-carrito/<int:pk>/', añadirCarrito.as_view(), name="añadirCarrito"),
    path('perfil/carrito/borrarProducto/<int:pk>/', borrarProductoCarrito.as_view(), name="borrarProductoCarrito"),
    #path('perfil/carrito', editarCarrito.as_view(), name="editarCarrito"),
    path('catalogo/h', views.catalogoH, name="catalogoH"),
    path('catalogo/m', views.catalogoM, name="catalogoM"),
    path('catalogo/no', views.catalogoNo, name="catalogoNo"),
    path('catalogo/na', views.catalogoNa, name="catalogoNa"),
    path('perfil/carrito/checkout/<int:pk>/', vistaCheckout.as_view(), name="checkout"),
    path('crear-checkout-session/<int:pk>/', views.crear_checkout_session),
    path('webhook/', views.stripe_webhook),
    path('contacto', views.contacto, name="contacto"),
    path('faq', views.faq, name="faq"),
    path('envios-devoluciones', views.enviosDevoluciones, name="envios-devoluciones"),
    path('nosotros', views.nosotros, name="nosotros"),
    path('producto/<int:pk>',views.productoSingle, name="productoSingle"),
    path('productov2/<int:pk>',views.productoSingle2.as_view(), name="productoSinglev2"),
    path('catalogo/filter', views.filtros.as_view(), name="filtros"),


    #BACKEND
    path('backend/', login_required(viewsBackend.indexList), name="indexBackend"),
    path('backend/login', LoginView.as_view(template_name='diverseBackend/login.html'),name="backendLogin"),
    path('backend/logout', login_required(logout_then_login),name="backendCerrarSesion"),
    path('backend/registar-usuario', login_required(viewsBackend.registarUsuarioBackend),name="backendRegistrarUsuario"),
    #path('backend/perfil', login_required(viewsBackend.perfil), name="backendPerfil"),
    path('backend/crear-color', login_required(viewsBackend.crearColor), name="crearColor"),
    path('backend/crear-talla', login_required(viewsBackend.crearTalla), name="crearTalla"),
    path('backend/crear-categoria', login_required(viewsBackend.crearCategoria), name="crearCategoria"),
    path('backend/crear-subcategoria', login_required(viewsBackend.crearSubCategoria), name="crearSubCategoria"),
    path('backend/crear-marca', login_required(viewsBackend.crearMarca), name="crearMarca"),
    path('backend/crear-modelo', login_required(viewsBackend.crearModelo), name="crearModelo"),
    path('backend/crear-producto', login_required(viewsBackend.crearProducto.as_view()), name="crearProducto"),
    path('backend/ver-color', login_required(viewsBackend.verColor), name="verColor"),    
    path('backend/ver-sexo', login_required(viewsBackend.verSexo), name="verSexo"),    
    path('backend/ver-talla',login_required(viewsBackend.verTalla), name="verTalla"),    
    path('backend/ver-categoria',login_required(viewsBackend.verCategoria), name="verCategoria"),    
    path('backend/ver-subcategoria',login_required(viewsBackend.verSubCategoria), name="verSubCategoria"),    
    path('backend/ver-marca', login_required(viewsBackend.verMarca), name= "verMarca"),    
    path('backend/ver-modelo', login_required(viewsBackend.verModelo), name= "verModelo"),    
    path('backend/ver-producto', login_required(viewsBackend.verProducto.as_view()), name= "verProducto"),
    path('backend/editar-color/<int:pk>', login_required(viewsBackend.editarColor.as_view()), name="editarColor"),
    path('backend/editar-talla/<int:pk>', login_required(viewsBackend.editarTalla.as_view()), name="editarTalla"),
    path('backend/editar-categoria/<int:pk>', login_required(viewsBackend.editarCategoria.as_view()), name="editarCategoria"),
    path('backend/editar-subcategoria/<int:pk>', login_required(viewsBackend.editarSubCategoria.as_view()), name="editarSubcategoria"),
    path('backend/editar-marca/<int:pk>', login_required(viewsBackend.editarMarca.as_view()), name="editarMarca"),
    path('backend/editar-modelo/<int:pk>', login_required(viewsBackend.editarModelo.as_view()), name="editarModelo"),
    path('backend/editar-producto/<int:pk>', login_required(viewsBackend.editarProducto.as_view()), name="editarProducto"),
    path('backend/eliminar-producto/<int:pk>', login_required(viewsBackend.eliminarProducto), name="eliminarProducto"),
    path('backend/eliminar-color/<int:pk>', login_required(viewsBackend.eliminarColor), name="eliminarColor"),
    path('backend/eliminar-talla/<int:pk>', login_required(viewsBackend.eliminarTalla), name="eliminarTalla"),
    path('backend/eliminar-subcategoria/<int:pk>', login_required(viewsBackend.eliminarSubCategoria), name="eliminarSubCategoria"),
    path('backend/eliminar-modelo/<int:pk>', login_required(viewsBackend.eliminarModelo), name="eliminarModelo"),
    path('backend/eliminar-categoria/<int:pk>', login_required(viewsBackend.eliminarCategoria), name="eliminarCategoria"),
    path('backend/eliminar-marca/<int:pk>', login_required(viewsBackend.eliminarMarca), name="eliminarMarca"),

    path('backend/ver-stock', login_required(viewsBackend.verStock), name='verStock'),
   # path('backend/ver-stock/<int:pk>', viewsBackend.verStockSingle), name="verStockSingle"),
    path('backend/crear-stock/<int:pk>', login_required(crearStock.as_view()), name='crearStock'),
    path('backend/editar-stock/<int:pk>', login_required(editarStock.as_view()), name='editarStock'),
    path('backend/stock/add/<int:numRef>/<int:cantidad>', login_required(addStock.as_view()), name="addStock"),
    path('backend/stock/less/<int:numRef>/<int:cantidad>', login_required(lessStock.as_view()), name="lessStock"),


    path('backend/producto/<int:pk>', login_required(viewsBackend.verProductoSimple), name="verProductoSimple"),
    path('backend/imagenProducto/<int:primarykey>', login_required(viewsBackend.agregarFotos), name="agregarImagen"),
    path('backend/borrarImagenProducto/<int:pkproducto>/<int:pkfoto>', login_required(viewsBackend.eliminarFoto), name="borrarImagen"),

    path('activar-usuario/<uidb64>/<token>', views.activate_user, name='activar'),
    path('verification/', include('verify_email.urls')),


    path('ajax/load-modelos/', viewsBackend.load_modelos, name='ajax_load_modelos'),                            # AJAX
    path('ajax/load-subcategorias/', viewsBackend.load_subcategorias, name='ajax_load_subcategorias'),          # AJAX
    
]
handler404 = "diverse.views.page_not_found_view"

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

