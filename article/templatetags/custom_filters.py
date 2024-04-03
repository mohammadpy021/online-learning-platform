from django import template

register = template.Library()

@register.filter
def divide(value, arg):
    try:
        return int(value) / int(arg)
    except (ValueError, ZeroDivisionError):
        return None
    
@register.simple_tag
def modulo(value, arg):
    try:
        return int(value) % int(arg)
    except (ValueError, ZeroDivisionError):
        return None
    
