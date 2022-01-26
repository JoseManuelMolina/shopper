from django.shortcuts import render

# Create your views here.

def store(request):
    context = {}
    return render(request, 'diverse/store.html', context)

def cart(request):
    context = {}
    return render(request, 'diverse/cart.html', context)

def checkout(request):
    context = {}
    return render(request, 'diverse/checkout.html', context)