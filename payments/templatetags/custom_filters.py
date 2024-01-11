from django import template

register = template.Library()


@register.filter
def multiply_by_100(value):
    return value * 100
