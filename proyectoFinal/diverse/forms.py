from django import forms

from .models import *

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