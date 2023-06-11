import json

from django import template
from django.core.serializers import serialize
from django.utils.safestring import mark_safe

from oursite.models import *

register = template.Library()

@register.filter
def json(queryset):
    return serialize('json', queryset)

