from django import forms

from django.contrib.auth.models import User

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

class sexoForm(forms.Form):
    
    nombreSexo = forms.CharField(
        max_length=2,
        label='Sexo',
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'id':'nombreSexo',
                'placeHolder':'Símbolo Sexo'}
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


class subcategoriaForm(forms.Form):
    nombreSubcategoria = forms.CharField(
        max_length = 40,
        label = "Nombre de la subcategoria",
        widget = forms.TextInput(
            attrs={
                'class' : 'form-control',
                'id' : 'nombre',
                'placeholder' : 'Nombre'}
        )
    )

    categoria_id = forms.ChoiceField(
        label = "Categoria"
    )