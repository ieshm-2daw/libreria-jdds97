from biblioteca.models import Genero
from django import template

register = template.Library()


@register.simple_tag
def get_genero():
    return Genero.objects.all()
