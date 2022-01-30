from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required

from diverse.forms import *

from .models import *

# Create your views here.

# BACKEND

# class indexListView(ListView):
#    model = color
#    template_name = 'index.html'
#    content_object_name = 'indexList'

def indexList(request):
    colores = color.objects.all()
    return render(request, 'diverseBackend/index.html', {'colores': colores})

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