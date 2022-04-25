from unicodedata import name
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, logout_then_login

from . import viewsBackend
from . import views

from diverse.viewsBackend import *
from diverse.views import *

from django.conf import settings


urlpatterns = [
    #Deja la cadena vacía para usar la url base (/)
    path('', views.index, name="index"),
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

    path('backend/', viewsBackend.indexList, name="indexBackend"),
    path('backend/login', LoginView.as_view(template_name='diverseBackend/login.html'),name="backendLogin"),
    path('backend/logout', logout_then_login,name="backendCerrarSesion"),
    path('backend/perfil', viewsBackend.perfil, name="backendPerfil"),
    path('backend/crear-color', viewsBackend.crearColor, name="crearColor"),
    path('backend/ver-color',viewsBackend.verColor, name="verColor"),
    path('backend/crear-sexo', viewsBackend.crearSexo, name="crearSexo"),
    path('backend/ver-sexor',viewsBackend.verSexo, name="verSexo"),
    path('backend/crear-talla', viewsBackend.crearTalla, name="crearTalla"),
    path('backend/ver-talla',viewsBackend.verTalla, name="verTalla"),
    path('backend/crear-categoria', viewsBackend.crearCategoria, name="crearCategoria"),
    path('backend/ver-categoria',viewsBackend.verCategoria, name="verCategoria"),
    path('backend/crear-subcategoria', viewsBackend.crearSubCategoria, name="crearSubCategoria"),
    path('backend/ver-subcategoria',viewsBackend.verSubCategoria, name="verSubCategoria"),
    path('backend/crear-marca', viewsBackend.crearMarca, name="crearMarca"),
    path('backend/ver-marca', viewsBackend.verMarca, name= "verMarca"),
    path('backend/crear-modelo', viewsBackend.crearModelo, name="crearModelo"),
    path('backend/ver-modelo', viewsBackend.verModelo, name= "verModelo"),
    path('backend/crear-producto', viewsBackend.crearProducto, name="crearProducto"),
    path('backend/ver-producto', viewsBackend.verProducto, name= "verProducto"),
    
    
        
]
handler404 = "diverse.views.page_not_found_view"

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

