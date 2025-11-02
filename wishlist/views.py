from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Wishlist, WishlistItem
from products.models import Product


@login_required
def wishlist_detail(request):
    """Wishlist page"""
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    items = wishlist.items.select_related('product')
    
    return render(request, 'wishlist/wishlist_detail.html', {
        'wishlist': wishlist,
        'wishlist_items': items
    })


@login_required
def add_to_wishlist(request, product_id):
    """Add product to wishlist"""
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    
    # Check if product already in wishlist
    item, created = WishlistItem.objects.get_or_create(
        wishlist=wishlist,
        product=product
    )
    
    if created:
        messages.success(request, f'{product.name} added to wishlist!')
    else:
        messages.info(request, f'{product.name} is already in your wishlist.')
    
    return redirect(request.META.get('HTTP_REFERER', 'products:home'))


@login_required
def remove_from_wishlist(request, product_id):
    """Remove product from wishlist"""
    wishlist = get_object_or_404(Wishlist, user=request.user)
    item = get_object_or_404(WishlistItem, wishlist=wishlist, product_id=product_id)
    
    product_name = item.product.name
    item.delete()
    
    messages.success(request, f'{product_name} removed from wishlist!')
    return redirect('wishlist:wishlist_detail')
