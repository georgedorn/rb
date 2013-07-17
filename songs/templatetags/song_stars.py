from django import template
from django.utils.safestring import mark_safe

register = template.Library()

def stars(value, arg=None):
    tag = "<span class='stars-%s'><span>%s</span></span>" % (value, value)
    return mark_safe(tag)
stars.needs_autoescape=False

register.filter('stars',stars)
