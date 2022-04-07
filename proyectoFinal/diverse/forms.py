from cProfile import label
from dataclasses import fields
from tkinter import FLAT
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

    nombreSubcategoria = forms.CharField(
        max_length=40,
        label = 'Subcategoria',
        widget = forms.TextInput(
            attrs={
                'class' : 'form-control',
                'id' : 'nombreSubcategoria',
                'placeholder' : 'Nombre de la subcategoria'
            }
        )
    )

#    categoria_id = forms.ModelChoiceField(
#        queryset=categoria.objects.all().values_list('nombre', flat=True), empty_label=None)

    categoria_id = forms.ChoiceField(
            label='Categoria:',
            choices=categoria.objects.values_list('id','nombre')
        )

class marcaForm(forms.ModelForm):

    class Meta:
        model = marca
        fields = ('id', 'nombre')

    nombreMarca = forms.CharField(
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

    subCategoria_id = forms.ModelChoiceField(queryset = subCategoria.objects.all().values_list('id', flat = True), empty_label = None)