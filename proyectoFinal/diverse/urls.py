from django.urls import path

from . import viewsBackend
from . import views

from diverse.viewsBackend import *
from diverse.views import *

urlpatterns = [
    #Deja la cadena vacía para usar la url base (/)
    path('', views.index, name="index"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('backend/', viewsBackend.indexList, name="indexBackend"),
    path('backend/crear', viewsBackend.crearColor, name="crearColor"),
]