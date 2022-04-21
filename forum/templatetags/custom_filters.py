from django import template


register = template.Library()

def pass_key(d, key):
    # d is dict
    return d[key]

def get_elem(iterable, index):
    return iterable[index]

def multiply(constant, value):
    return constant * value

def deslugify(slug):
    slug = slug.split('-')
    slug[0] = slug[0].capitalize()
    return ' '.join(slug)

def make_chain(path):
    path = path.strip('/')
    path = path.split('/')
    if len(path) > 2:
        # /subforum/thread/ is as deep as it goes
        path = path[:2]
    else:
        path.pop(-1)

    chain = []
    link = '/'
    path_names = []
    for step in path:
        path_names.append(deslugify(step))
        link += step
        link += '/'
        chain.append(link)

    path_name_pairs = zip(path_names, chain)
    return path_name_pairs

register.filter('pass_key', pass_key)
register.filter('get_elem', get_elem)
register.filter('multiply', multiply)
register.filter('make_chain', make_chain)
