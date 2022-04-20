from django import template


register = template.Library()

def pass_key(d, key):
    # d is dict
    return d[key]

def get_elem(iterable, index):
    return iterable[index]

def multiply(constant, value):
    return constant * value

register.filter('pass_key', pass_key)
register.filter('get_elem', get_elem)
register.filter('multiply', multiply)
