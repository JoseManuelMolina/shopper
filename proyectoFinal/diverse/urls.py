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
    path('perfil/', views.perfil, name="perfil"),
    path('perfil/direcciones', views.direcciones.as_view(), name="direcciones"),
    #path('perfil/direcciones/añadir', views.crearDireccion.as_view(), name="añadirDireccion"),
    path('perfil/direcciones/añadir', views.crearDireccion, name="añadirDireccion"),
    path('perfil/direcciones/<int:pk>', views.editarDireccion.as_view(), name="editarDireccion"),
    path('cart/', views.cart, name="cart"),
    path('catalogo/h', views.catalogoH, name="catalogoH"),
    path('catalogo/m', views.catalogoM, name="catalogoM"),
    path('catalogo/no', views.catalogoNo, name="catalogoNo"),
    path('catalogo/na', views.catalogoNa, name="catalogoNa"),
    path('checkout/', views.checkout, name="checkout"),
    path('login', LoginView.as_view(template_name='diverse/login.html'),name="login"),
    path('contacto', views.contacto, name="contacto"),
    path('faq', views.faq, name="faq"),
    path('envios-devoluciones', views.enviosDevoluciones, name="envios-devoluciones"),
    path('nosotros', views.nosotros, name="nosotros"),


    #BACKEND
    path('backend/', viewsBackend.indexList, name="indexBackend"),
    path('backend/login', LoginView.as_view(template_name='diverseBackend/login.html'),name="backendLogin"),
    path('backend/logout', logout_then_login,name="backendCerrarSesion"),
    path('backend/perfil', viewsBackend.perfil, name="backendPerfil"),
    path('backend/crear-color', viewsBackend.crearColor, name="crearColor"),
    path('backend/crear-talla', viewsBackend.crearTalla, name="crearTalla"),
    path('backend/crear-categoria', viewsBackend.crearCategoria, name="crearCategoria"),
    path('backend/crear-subcategoria', viewsBackend.crearSubCategoria, name="crearSubCategoria"),
    path('backend/crear-marca', viewsBackend.crearMarca, name="crearMarca"),
    path('backend/crear-modelo', viewsBackend.crearModelo, name="crearModelo"),
    path('backend/crear-producto', viewsBackend.crearProducto.as_view(), name="crearProducto"),
    path('backend/ver-color',viewsBackend.verColor, name="verColor"),    
    path('backend/ver-sexo',viewsBackend.verSexo, name="verSexo"),    
    path('backend/ver-talla',viewsBackend.verTalla, name="verTalla"),    
    path('backend/ver-categoria',viewsBackend.verCategoria, name="verCategoria"),    
    path('backend/ver-subcategoria',viewsBackend.verSubCategoria, name="verSubCategoria"),    
    path('backend/ver-marca', viewsBackend.verMarca, name= "verMarca"),    
    path('backend/ver-modelo', viewsBackend.verModelo, name= "verModelo"),    
    path('backend/ver-producto', viewsBackend.verProducto.as_view(), name= "verProducto"),
    path('backend/editar-color/<int:pk>', viewsBackend.editarColor.as_view(), name="editarColor"),
    path('backend/editar-talla/<int:pk>', viewsBackend.editarTalla.as_view(), name="editarTalla"),
    path('backend/editar-categoria/<int:pk>', viewsBackend.editarCategoria.as_view(), name="editarCategoria"),
    path('backend/editar-subcategoria/<int:pk>', viewsBackend.editarSubCategoria.as_view(), name="editarSubcategoria"),
    path('backend/editar-marca/<int:pk>', viewsBackend.editarMarca.as_view(), name="editarMarca"),
    path('backend/editar-modelo/<int:pk>', viewsBackend.editarModelo.as_view(), name="editarModelo"),
    path('backend/editar-producto/<int:pk>', viewsBackend.editarProducto.as_view(), name="editarProducto"),


    path('ajax/load-modelos/', viewsBackend.load_modelos, name='ajax_load_modelos'),                            # AJAX
    path('ajax/load-subcategorias/', viewsBackend.load_subcategorias, name='ajax_load_subcategorias'),          # AJAX
    
    
        
]
handler404 = "diverse.views.page_not_found_view"

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

