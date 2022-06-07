from cProfile import label
from dataclasses import fields
from tkinter import FLAT
from tkinter.tix import Select
from typing import Type
from django import forms

from django.contrib.auth.models import User
from django.urls import clear_script_prefix

from diverse.models import *
from account.models import *

from django.db import models
from django.forms import ModelChoiceField, ModelForm


# FORM FRONTEND

class infoPersonal(forms.ModelForm):

    class Meta:
        model = Account
        fields = ('nombre', 'apellidos', 'username', 'telefono', 'email', 'password', 'fechaNacimiento', 'genero')

class direccionesForm(forms.ModelForm):

    class Meta:
        model = direccion
        fields = '__all__'
        

# FORM BACKEND

class usuarioForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = '__all__'
        

class imagenUsuario(forms.ModelForm):

    class Meta:
        model = Account
        fields = ('imagen_perfil',)
        
    imagen_perfil = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'class': 'form-control',
                'enctype':'multipart/form-data'
                }
            )
        )

class colorForm(forms.ModelForm):

    class Meta:
        model = color
        fields = ('id', 'nombre', 'hexcolor')

#    def __init__(self, *args, **kwargs):
#        super(sexoForm, self).__init__(*args, **kwargs)
#        self.fields['tipo'].widget.attrs = {
#            'class':'form-control',
#            'id':'tipo',
#            'placeHolder':'Símbolo Sexo'
#        }

class sexoForm(forms.ModelForm):
    
    class Meta:
        model = sexo
        fields = ('id', 'tipo')

    def __init__(self, *args, **kwargs):
        super(sexoForm, self).__init__(*args, **kwargs)
        self.fields['tipo'].widget.attrs = {
            'class':'form-control',
            'id':'tipo',
            'placeHolder':'Símbolo Sexo'
        }

    def comprobarTipo(self):
        tipo = self.cleaned_data.get('tipo')
        if(tipo == ""):
            raise forms.ValidationError('Este campo no se puede dejar vacío')

        for instance in sexo.objects.all():
            if instance.tipo == tipo:
                raise forms.ValidationError('Ya existe un tipo con este valor')
        return tipo

class tallaForm(forms.ModelForm):

    class Meta:
        model = talla
        fields = ('id', 'nombre')

class categoriaForm(forms.ModelForm):

    class Meta:
        model = categoria
        fields = ('id', 'nombre')
#        read_only_fields = ('id', 'nombre')

#    sexo_id = forms.ChoiceField(
#        label='Sexo:',
#        choices=sexo.objects.values_list('id','tipo')
#    )

#    def __init__(self, *args, **kwargs):
#        super(categoriaForm, self).__init__(*args, **kwargs)
#        self.fields['sexo_id'].widget.attrs = {
#            'class':'form-control',
#            'id':'tipo',
#            'placeHolder':'Símbolo Sexo'
#        }

    #sexo_id = forms.ModelChoiceField( queryset=sexo.objects.all(), to_field_name="id", empty_label=None)
    #sexo_id = forms.ModelChoiceField()
        
class subcategoriaForm(forms.ModelForm):

    class Meta:
        model = subCategoria
        fields = ('id', 'nombre')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        choicesCategoria = [('-1', '---- Selecciona la categoria del producto ----')]
        choicesCategoria.extend([(categoria.id, categoria.nombre) for categoria in categoria.objects.all().order_by('nombre')])
        self.fields['categoria_id'].choices = choicesCategoria
        self.fields['categoria_id'].widget.disabled_choices = [-1]
        self.initial['categoria_id'] = -1


#    categoria_id = forms.ModelChoiceField(
#        queryset=categoria.objects.all().values_list('nombre', flat=True), empty_label=None)

    nombre = forms.CharField(
        max_length = 60,
        label = 'SubCategoria',
        widget = forms.TextInput(
            attrs = {
                'class' : 'form-control',
                'id' : 'nombreSubCategoria',
                'placeholder' : 'Nombre de la SubCategoria'
            }
        )
    )

    categoria_id = forms.ChoiceField(
            label='Categoria:',
            choices=categoria.objects.all().values_list('id','nombre'),
            widget = forms.Select(
            attrs = {
                'class' : 'form-control',
                'id' : 'categoriaID'
            }
        )
    )

class marcaForm(forms.ModelForm):

    class Meta:
        model = marca
        fields = ('id', 'nombre')

class modeloForm(forms.ModelForm):

    class Meta:
        model = modelo
        fields = ('id', 'nombre')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        choicesMarca = [('-1', '---- Selecciona la marca del producto ----')]
        choicesMarca.extend([(marca.id, marca.nombre) for marca in marca.objects.all().order_by('nombre')])
        self.fields['marca_id'].choices = choicesMarca
        self.fields['marca_id'].widget.disabled_choices = [-1]
        self.initial['marca_id'] = -1

    nombre = forms.CharField(
        max_length = 60,
        label = 'Modelo',
        widget = forms.TextInput(
            attrs = {
                'class' : 'form-control',
                'id' : 'nombreModelo',
                'placeholder' : 'Nombre del modelo'
            }
        )
    )

    marca_id = forms.ChoiceField(
            label='Marca:',
            choices=marca.objects.all().values_list('id','nombre'),
            widget = forms.Select(
            attrs = {
                'class' : 'form-control',
                'id' : 'nombreMarca'
            }
        )
    )

class productoForm(forms.ModelForm):

    class Meta:
        model = producto
        fields = ('num_ref', 'sexo', 'categoria', 'subCategoria', 'marca', 'modelo', 'color', 'talla', 'precio', 'imagen')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['modelo'].queryset = modelo.objects.none()  #Coge el campo modelo y lo vacia
        self.fields['subCategoria'].queryset = subCategoria.objects.none()  #Coge el campo modelo y lo vacia        

        if 'marca' in self.data:
            try:
                marca_id = int(self.data.get('marca'))
                self.fields['modelo'].queryset = modelo.objects.filter(marca_id = marca_id).order_by('nombre')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['modelo'].queryset = self.instance.marca.modelo_set.order_by('nombre')

        if 'categoria' in self.data:
            try:
                categoria_id = int(self.data.get('categoria'))
                self.fields['subCategoria'].queryset = subCategoria.objects.filter(categoria_id = categoria_id).order_by('nombre')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['subCategoria'].queryset = self.instance.categoria.subcategoria_set.order_by('nombre')

class imagenProductoForm(ModelForm):
    class Meta:
        model = imagenProducto
        fields = ['imagen'] 


