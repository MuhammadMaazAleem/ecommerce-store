from django.db import models
from django.conf import settings
from products.models import Product


class Wishlist(models.Model):
    """User wishlist"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlist')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Wishlist for {self.user.username}"
    
    @property
    def total_items(self):
        return self.items.count()


class WishlistItem(models.Model):
    """Items in wishlist"""
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.product.name} in {self.wishlist.user.username}'s wishlist"
    
    class Meta:
        unique_together = ['wishlist', 'product']
        ordering = ['-added_at']
