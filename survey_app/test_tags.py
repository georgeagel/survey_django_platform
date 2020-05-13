from django import template

register = template.Library()

@register.filter
def intcomma(value):
    return value + 1    