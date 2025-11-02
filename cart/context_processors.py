from .cart import Cart


def cart(request):
    """Make cart available in all templates"""
    return {'cart': Cart(request)}
