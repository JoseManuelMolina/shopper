from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from diverse.forms import *

from diverse.models import *
from account.models import *

# Create your views here.

# BACKEND

# class indexListView(ListView):
#    model = color
#    template_name = 'index.html'
#    content_object_name = 'indexList'

def indexList(request):
    colores = color.objects.all()
    sexos = sexo.objects.all()
    tallas = talla.objects.all()
    return render(request, 'diverseBackend/index.html', {'colores': colores, 'sexos':sexos, 'tallas': tallas})

@login_required(login_url='backendLogin')
def perfil(request):
    if request.method == 'POST':
        form = usuarioForm(request.POST, request.FILES, request.user)
        if form.is_valid():
            form.save()
            return redirect('backendPerfil')
    else:
        usuario = request.user
        form = usuarioForm(usuario)
    
    return render(request, 'diverseBackend/perfil.html', {'form':form, 'usuario':usuario})

@login_required(login_url='backendLogin')
def crearColor(request):
    if request.method == 'POST':
        form = colorForm(request.POST)
        if form.is_valid():
            colorDatosForm = form.cleaned_data

            colorDatos = color(
                nombre = colorDatosForm['nombreColor'],
            )

            colorDatos.save()
        return redirect('indexBackend')
    else:
        form = colorForm()
    
    return render(request, 'diverseBackend/color_form.html', {'form':form})

@login_required(login_url='backendLogin')
def crearSexo(request):
    if request.method == 'POST':
        form = sexoForm(request.POST)
        if form.is_valid():
            sexoDatosForm = form.cleaned_data

            sexoDatos = sexo(
                tipo = sexoDatosForm['nombreSexo'],
            )

            sexoDatos.save()
        return redirect('indexBackend')
    else:
        form = sexoForm()
    
    return render(request, 'diverseBackend/sexo_form.html', {'form':form})

@login_required(login_url='backendLogin')
def crearTalla(request):
    if request.method == 'POST':
        form = tallaForm(request.POST)
        if form.is_valid():
            tallaDatosForm = form.cleaned_data

            tallaDatos = talla(
                nombre = tallaDatosForm['nombreTalla'],
            )

            tallaDatos.save()
        return redirect('indexBackend')
    else:
        form = tallaForm()
    
    return render(request, 'diverseBackend/talla_form.html', {'form':form})