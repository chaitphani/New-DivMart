from django import template

register = template.Library()

@register.filter(name='spread')
def cut(value, arg):
    return value.split(arg)