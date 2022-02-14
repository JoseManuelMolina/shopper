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
    path('checkout/', views.checkout, name="checkout"),
    path('login', LoginView.as_view(template_name='diverse/login.html'),name="login"),

    path('backend/', viewsBackend.indexList, name="indexBackend"),
    path('backend/login', LoginView.as_view(template_name='diverseBackend/login.html'),name="backendLogin"),
    path('backend/logout', logout_then_login,name="backendCerrarSesion"),
    path('backend/perfil', viewsBackend.perfil, name="backendPerfil"),
    path('backend/crear-color', viewsBackend.crearColor, name="crearColor"),
    path('backend/crear-sexo', viewsBackend.crearSexo, name="crearSexo"),
    path('backend/crear-talla', viewsBackend.crearTalla, name="crearTalla"),
    path('backend/crear-categoria', viewsBackend.crearCategoria, name="crearCategoria"),

        
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)