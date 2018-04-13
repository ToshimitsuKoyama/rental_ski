from django import template

from django.utils.safestring import mark_safe
from django.template import Library

import json


register = Library()


@register.filter(is_safe=True)
def js(obj):
    return mark_safe(obj)


@register.filter
def get_at_index(list_date, index):
    return list_date[index]
