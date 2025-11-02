from products.models import Product, ProductVariant


class Cart:
    """Shopping cart class for session-based cart"""
    
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart
    
    def add(self, product, variant=None, quantity=1, update_quantity=False):
        """Add product to cart or update quantity"""
        product_id = str(product.id)
        variant_id = str(variant.id) if variant else None
        
        # Create cart key
        cart_key = f"{product_id}"
        if variant_id:
            cart_key += f"-{variant_id}"
        
        if cart_key not in self.cart:
            self.cart[cart_key] = {
                'product_id': product_id,
                'variant_id': variant_id,
                'quantity': 0,
                'price': str(product.price)
            }
        
        if update_quantity:
            self.cart[cart_key]['quantity'] = quantity
        else:
            self.cart[cart_key]['quantity'] += quantity
        
        self.save()
    
    def save(self):
        """Save cart to session"""
        self.session.modified = True
    
    def remove(self, product_id, variant_id=None):
        """Remove product from cart"""
        cart_key = str(product_id)
        if variant_id:
            cart_key += f"-{variant_id}"
        
        if cart_key in self.cart:
            del self.cart[cart_key]
            self.save()
    
    def update_quantity(self, product_id, variant_id, quantity):
        """Update product quantity"""
        cart_key = str(product_id)
        if variant_id:
            cart_key += f"-{variant_id}"
        
        if cart_key in self.cart:
            self.cart[cart_key]['quantity'] = quantity
            self.save()
    
    def clear(self):
        """Clear cart"""
        del self.session['cart']
        self.save()
    
    def __iter__(self):
        """Iterate over cart items"""
        product_ids = [int(item['product_id']) for item in self.cart.values()]
        products = Product.objects.filter(id__in=product_ids)
        
        cart = self.cart.copy()
        for product in products:
            for key, item in cart.items():
                if item['product_id'] == str(product.id):
                    item['product'] = product
                    item['total_price'] = float(item['price']) * item['quantity']
                    
                    # Get variant if exists
                    if item.get('variant_id'):
                        try:
                            variant = ProductVariant.objects.get(id=int(item['variant_id']))
                            item['variant'] = variant
                        except ProductVariant.DoesNotExist:
                            pass
                    
                    yield item
    
    def __len__(self):
        """Count cart items"""
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_total_price(self):
        """Calculate total price"""
        return sum(float(item['price']) * item['quantity'] for item in self.cart.values())
    
    def get_subtotal(self):
        """Get subtotal"""
        return self.get_total_price()
