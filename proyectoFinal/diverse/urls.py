from django.urls import path

from . import viewsBackend
from . import views

urlpatterns = [
    #Deja la cadena vacía para usar la url base (/)
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('backend/', viewsBackend.index, name="indexBackend"),
]