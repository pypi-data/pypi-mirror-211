'''potentially universally unique phrase'''

__version__ = '0.1.0'

from puup.render import render


def puup(template='rran'):
    return tuple(render(template))


__all__ = ['puup']
