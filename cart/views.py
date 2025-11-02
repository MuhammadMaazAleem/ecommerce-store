from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from products.models import Product, ProductVariant
from .cart import Cart


def cart_detail(request):
    """Cart detail page"""
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})


@require_POST
def cart_add(request, product_id):
    """Add product to cart"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    variant_id = request.POST.get('variant_id')
    variant = None
    
    if variant_id:
        variant = get_object_or_404(ProductVariant, id=variant_id)
    
    quantity = int(request.POST.get('quantity', 1))
    cart.add(product=product, variant=variant, quantity=quantity)
    
    messages.success(request, f'{product.name} added to cart!')
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    """Remove product from cart"""
    cart = Cart(request)
    variant_id = request.POST.get('variant_id')
    cart.remove(product_id, variant_id)
    
    messages.success(request, 'Item removed from cart!')
    return redirect('cart:cart_detail')


@require_POST
def cart_update(request, product_id):
    """Update cart item quantity"""
    cart = Cart(request)
    variant_id = request.POST.get('variant_id')
    quantity_str = request.POST.get('quantity', '1')
    
    # Handle empty string
    try:
        quantity = int(quantity_str) if quantity_str else 1
    except (ValueError, TypeError):
        quantity = 1
    
    if quantity > 0:
        cart.update_quantity(product_id, variant_id, quantity)
        messages.success(request, 'Cart updated!')
    else:
        cart.remove(product_id, variant_id)
        messages.success(request, 'Item removed from cart!')
    
    return redirect('cart:cart_detail')
