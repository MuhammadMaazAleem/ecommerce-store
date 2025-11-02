from .models import Wishlist


def wishlist(request):
    """Make wishlist available in all templates"""
    wishlist_count = 0
    if request.user.is_authenticated:
        try:
            wishlist_obj = Wishlist.objects.get(user=request.user)
            wishlist_count = wishlist_obj.total_items
        except Wishlist.DoesNotExist:
            pass
    
    return {'wishlist_count': wishlist_count}
