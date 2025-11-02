from django.db import models
from django.conf import settings
from products.models import Product, ProductVariant


class Cart(models.Model):
    """Shopping cart for logged-in users"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Cart for {self.user.username}"
    
    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())
    
    @property
    def subtotal(self):
        return sum(item.total_price for item in self.items.all())
    
    @property
    def total_price(self):
        # Can add tax, shipping, discounts here
        return self.subtotal


class CartItem(models.Model):
    """Items in shopping cart"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    @property
    def unit_price(self):
        price = self.product.price
        if self.variant:
            price += self.variant.price_adjustment
        return price
    
    @property
    def total_price(self):
        return self.unit_price * self.quantity
    
    class Meta:
        unique_together = ['cart', 'product', 'variant']
