from django import template


register = template.Library()

def pass_key(context, key):
    return context[key]

register.filter('pass_key', pass_key)
