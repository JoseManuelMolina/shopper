from django import template

register = template.Library()

@register.filter
def in_categoria(subcategorias, categoria):
    return subcategorias.filter(categoria=categoria)