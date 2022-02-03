from django import forms

from diverse.models import *
from account.models import *

class usuarioForm(forms.Form):

    email = forms.CharField(
        max_length=100,
        label='email',
        widget=forms.TextInput(
            attrs={
                'class':'form-control', 
                'id':'email',
                'placeholder':'Email',
                'value':'{{ usuario.email }}'}
        )
    )

    username = forms.CharField(
        max_length=50,
        label='username',
        widget=forms.TextInput(
            attrs={
                'class':'form-control', 
                'id':'username',
                'placeholder':'Nombre de usuario',
                'value':'{{ usuario.username }}'}
        )
    )

    nombre = forms.CharField(
        max_length=20,
        label='nombre',
        widget=forms.TextInput(
            attrs={
                'class':'form-control', 
                'id':'nombre',
                'placeholder':'Nombre',
                'value':'{{ usuario.nombre }}'}
        )
    )

    apellidos = forms.CharField(
        max_length=60,
        label='apellidos',
        widget=forms.TextInput(
            attrs={
                'class':'form-control', 
                'id':'apellidos',
                'placeholder':'Apellidos',
                'value':'{{ usuario.apellidos }}'}
        )
    )

    direccion = forms.CharField(
        max_length=100,
        label='direccion',
        widget=forms.TextInput(
            attrs={
                'class':'form-control', 
                'id':'direccion',
                'placeholder':'Dirección',
                'value':'{{ usuario.direccion }}'}
        )
    )

    pais = forms.CharField(
        max_length=40,
        label='pais',
        widget=forms.TextInput(
            attrs={
                'class':'form-control', 
                'id':'pais',
                'placeholder':'País',
                'value':'{{ usuario.pais }}'}
        )
    )

    provincia = forms.CharField(
        max_length=40,
        label='provincia',
        widget=forms.TextInput(
            attrs={
                'class':'form-control', 
                'id':'provincia',
                'placeholder':'Provincia',
                'value':'{{ usuario.provincia }}'}
        )
    )

    localidad = forms.CharField(
        max_length=40,
        label='localidad',
        widget=forms.TextInput(
            attrs={
                'class':'form-control', 
                'id':'localidad',
                'placeholder':'Localidad',
                'value':'{{ usuario.localidad }}'}
        )
    )

    codigoPostal = forms.IntegerField(
        label='codigoPostal',
        widget=forms.NumberInput(
            attrs={
                'class':'form-control', 
                'id':'codigoPostal',
                'placeholder':'Código Postal',
                'value':'{{ usuario.codigoPostal }}'}
        )
    )

    telefono = forms.IntegerField(
        label='telefono',
        widget=forms.NumberInput(
            attrs={
                'class':'form-control', 
                'id':'telefono',
                'placeholder':'Teléfono',
                'value':'{{ usuario.telefono }}'}
        )
    )

    imagenPerfil = forms.ImageField(
        label='imagenPerfil',
        widget=forms.FileInput(
            attrs={
                'class':'form-control', 
                'id':'imagenPerfil',
                'value':'{{ usuario.imagen_perfil }}'}
        )
    )

class colorForm(forms.Form):

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

class categoriaForm(forms.Form):
    
    nombreCategoria = forms.CharField(
        max_length=2,
        label='nombreCategoria',
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'id':'nombreCategoria',
                'placeHolder':'Símbolo Categoría'}
        )
    )


class tallaForm(forms.Form):
    nombreTalla = forms.CharField(
        max_length=10,
        label="talla",
        widget=forms.TextInput(
            attrs={
                'class' : 'form-control',
                'id':'talla',
                'placeholder':'Talla'}
        )
    )