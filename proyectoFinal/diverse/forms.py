from cProfile import label
from dataclasses import fields
from tkinter import FLAT
from typing import Type
from django import forms

from django.contrib.auth.models import User
from django.urls import clear_script_prefix

from diverse.models import *
from account.models import *

from django.db import models
from django.forms import ModelChoiceField, ModelForm


class usuarioForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ('email', 'username', 'nombre', 'apellidos','direccion','pais','provincia','localidad','codigoPostal','telefono','imagen_perfil')

    email = forms.CharField(
        max_length=100,
        label='email',
        widget=forms.TextInput(
            attrs={
                'class':'form-control', 
                'id':'email',
                'placeholder':'Email'}
        )
    )

    username = forms.CharField(
        max_length=50,
        label='username',
        widget=forms.TextInput(
            attrs={
                'class':'form-control', 
                'id':'username',
                'placeholder':'Nombre de usuario'}
        )
    )

    nombre = forms.CharField(
        max_length=20,
        label='nombre',
        required=False,
        widget=forms.TextInput(
            attrs={
                'class':'form-control', 
                'id':'nombre',
                'placeholder':'Nombre'}
        )
    )

    apellidos = forms.CharField(
        max_length=60,
        label='apellidos',
        required=False,
        widget=forms.TextInput(
            attrs={
                'class':'form-control', 
                'id':'apellidos',
                'placeholder':'Apellidos'}
        )
    )

    direccion = forms.CharField(
        max_length=100,
        label='direccion',
        required=False,
        widget=forms.TextInput(
            attrs={
                'class':'form-control', 
                'id':'direccion',
                'placeholder':'Dirección'}
        )
    )

    pais = forms.CharField(
        max_length=40,
        label='pais',
        required=False,
        widget=forms.TextInput(
            attrs={
                'class':'form-control', 
                'id':'pais',
                'placeholder':'País'}
        )
    )

    provincia = forms.CharField(
        max_length=40,
        label='provincia',
        required=False,
        widget=forms.TextInput(
            attrs={
                'class':'form-control', 
                'id':'provincia',
                'placeholder':'Provincia'}
        )
    )

    localidad = forms.CharField(
        max_length=40,
        label='localidad',
        required=False,
        widget=forms.TextInput(
            attrs={
                'class':'form-control', 
                'id':'localidad',
                'placeholder':'Localidad'}
        )
    )

    codigoPostal = forms.IntegerField(
        label='codigoPostal',
        required=False,
        widget=forms.NumberInput(
            attrs={
                'class':'form-control', 
                'id':'codigoPostal',
                'placeholder':'Código Postal'}
        )
    )

    telefono = forms.IntegerField(
        label='telefono',
        required=False,
        widget=forms.NumberInput(
            attrs={
                'class':'form-control', 
                'id':'telefono',
                'placeholder':'Teléfono'}
        )
    )

    imagenPerfil = forms.ImageField(
        label='imagenPerfil',
        widget=forms.FileInput(
            attrs={
                'class':'form-control-file', 
                'id':'imagenPerfil'}
        )
    )

    def __init__(self, usuario, *args, **kwargs):
        super(usuarioForm, self).__init__(*args, **kwargs)
        
        self.fields['email'].initial = usuario.email
        self.fields['username'].initial = usuario.username
        self.fields['nombre'].initial = usuario.nombre
        self.fields['apellidos'].initial = usuario.apellidos
        self.fields['direccion'].initial = usuario.direccion
        self.fields['pais'].initial = usuario.pais
        self.fields['provincia'].initial = usuario.provincia
        self.fields['localidad'].initial = usuario.localidad
        self.fields['codigoPostal'].initial = usuario.codigoPostal
        self.fields['telefono'].initial = usuario.telefono

class colorForm(forms.ModelForm):

    class Meta:
        model = color
        fields = ('id', 'nombre')

    nombreColor = forms.CharField(
        max_length=60,
        label='nombreColor',
        widget=forms.TextInput(
            attrs={
                'class':'form-control', 
                'id':'nombreColor', 
                'placeholder':'Nombre Color'}
        )
    )

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

    tipo = forms.ChoiceField(
        label='Sexo:',
        choices=sexo.OPCIONES_SEXO,
    )

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

    nombre = forms.CharField(
        max_length=10,
        label="talla",
        widget=forms.TextInput(
            attrs={
                'class' : 'form-control',
                'id':'talla',
                'placeholder':'Talla'}
        )
    )

class categoriaForm(forms.ModelForm):

    class Meta:
        model = categoria
        fields = ('id', 'nombre')
#        read_only_fields = ('id', 'nombre')
    
    nombre = forms.CharField(
        max_length=40,
        label = 'Categoria',
         widget= forms.TextInput(
             attrs={
                'class':'form-control',
                'id': 'nombre',
                'placeholder':'Nombre de la categoria'
            }
        )
    ) 

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

    nombre = forms.CharField(
        max_length=40,
        label = 'Subcategoria',
        widget = forms.TextInput(
            attrs={
                'class' : 'form-control',
                'id' : 'nombre',
                'placeholder' : 'Nombre de la subcategoria'
            }
        )
    )

#    categoria_id = forms.ModelChoiceField(
#        queryset=categoria.objects.all().values_list('nombre', flat=True), empty_label=None)

    categoria_id = forms.ChoiceField(
            label='Categoria:',
            choices=categoria.objects.all().values_list('id','nombre')
        )

class marcaForm(forms.ModelForm):

    class Meta:
        model = marca
        fields = ('id', 'nombre')

    nombre = forms.CharField(
        max_length = 60,
        label = 'Marca',
        widget = forms.TextInput(
            attrs = {
                'class' : 'form-control',
                'id' : 'nombreMarca',
                'placeholder' : 'Nombre de la marca'
            }
        )
    )

class modeloForm(forms.ModelForm):

    class Meta:
        model = modelo
        fields = ('id', 'nombre')

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
            choices=marca.objects.all().values_list('id','nombre')
        )

class productoForm(forms.ModelForm):

    class Meta:
        model = producto
        #fields = ('num_ref', 'precio', 'imagen')
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['modelo'].queryset = modelo.objects.none()  #Coge el campo modelo y lo vacia
        self.fields['subCategoria'].queryset = subCategoria.objects.none()  #Coge el campo modelo y lo vacia

        if 'marca' in self.data:
            try:
                marca_id = int(self.data.get('marca'))
                self.fields['modelo'].queryset = modelo.objects.filter(marca_id = marca_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['modelo'].queryset = self.instance.marca.modelo_set.order_by()

        if 'categoria' in self.data:
            try:
                categoria_id = int(self.data.get('categoria'))
                self.fields['subCategoria'].queryset = subCategoria.objects.filter(categoria_id = categoria_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['subCategoria'].queryset = self.instance.categoria.subcategoria_set.order_by()

        

    num_ref = forms.CharField(
        max_length = 60,
        widget = forms.HiddenInput(
            attrs = {
                'class' : 'form-control',
                'id' : 'numrefProducto',
            }
        )
    )

    precio = forms.CharField(
        max_length = 60,
        label = 'Precio:',
        widget = forms.NumberInput(
            attrs = {
                'class' : 'form-control',
                'id' : 'precioProducto',
                'placeholder' : 'Precio del producto'
            }
        )
    )

    imagen = forms.FileField(
        max_length = 60,
        label = 'Imagen del producto:',
        widget = forms.FileInput(
            attrs = {
                'class':"form-control input-form",
                'id' : 'imagenProducto',
            }
        )
    )

    sexo_id = forms.ChoiceField(
        label='Sexo:',
        choices=sexo.objects.all().values_list('id','tipo'),
        widget = forms.Select(
            attrs = {
                'class':"form-control",
                'id' : 'sexoProducto',
            }
        )
    )

    categoria_id = forms.ChoiceField(
        label='Categoría:',
        choices=categoria.objects.all().values_list('id','nombre'),
        widget = forms.Select(
            attrs = {
                'class':"form-control",
                'id' : 'categoriaProducto',
            }
        )
    )

    subCategoria_id = forms.ChoiceField(
        label='Subcategoría:',
        #choices=subCategoria.objects.all().values_list('id','nombre'),
        widget = forms.Select(
            attrs = {
                'class':"form-control",
                'id' : 'subcategoriaProducto',
            }
        )
    )

    marca_id = forms.ChoiceField(
        label='Marca:',
        choices=marca.objects.all().values_list('id','nombre'),
        widget = forms.Select(
            attrs = {
                'class':"form-control",
                'id' : 'marcaProducto',
            }
        )
    )

<<<<<<< HEAD
=======
    

>>>>>>> bc50e8369a3cf4671aee59119ad43c39bf93e8de
    modelo_id = forms.ChoiceField(
        label='Modelo:',
        #choices=modelo.objects.filter(marca=aux).values_list('id','nombre'),
        #choices=modelo.objects.all().values_list('id','nombre'),
        widget = forms.Select(
            attrs = {
                'class':"form-control",
                'id' : 'modeloProducto',
            }
        )
    )

    color_id = forms.ChoiceField(
        label='Color:',
        choices=color.objects.all().values_list('id','nombre'),
        widget = forms.Select(
            attrs = {
                'class':"form-control",
                'id' : 'colorProducto',
            }
        )
    )

    talla_id = forms.ChoiceField(
        label='Talla:',
        choices=talla.objects.all().values_list('id','nombre'),
        widget = forms.Select(
            attrs = {
                'class':"form-control",
                'id' : 'tallaProducto',
            }
        )
    )