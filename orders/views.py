from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Order, OrderItem, OrderStatusHistory
from .emails import send_order_confirmation_email
from cart.cart import Cart
from accounts.forms import AddressForm


@login_required
def checkout(request):
    """Checkout page"""
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, 'Your cart is empty!')
        return redirect('products:product_list')
    
    addresses = request.user.addresses.all()
    
    context = {
        'cart': cart,
        'addresses': addresses,
    }
    return render(request, 'orders/checkout.html', context)


@login_required
def create_order(request):
    """Create order from cart"""
    if request.method != 'POST':
        return redirect('orders:checkout')
    
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, 'Your cart is empty!')
        return redirect('products:product_list')
    
    # Get shipping address from form
    first_name = request.POST.get('first_name', '')
    last_name = request.POST.get('last_name', '')
    shipping_name = f"{first_name} {last_name}".strip()
    shipping_phone = request.POST.get('phone')
    shipping_address1 = request.POST.get('address_line1')
    shipping_address2 = request.POST.get('address_line2', '')
    shipping_city = request.POST.get('city')
    shipping_state = request.POST.get('state')
    shipping_country = request.POST.get('country')
    shipping_postal = request.POST.get('postal_code')
    
    # Calculate totals
    subtotal = cart.get_subtotal()
    tax = subtotal * 0.10  # 10% tax
    shipping_cost = 500.00  # PKR 500 flat rate
    total = subtotal + tax + shipping_cost
    
    # Create order
    order = Order.objects.create(
        user=request.user,
        subtotal=subtotal,
        tax=tax,
        shipping_cost=shipping_cost,
        total=total,
        shipping_full_name=shipping_name,
        shipping_phone=shipping_phone,
        shipping_address_line1=shipping_address1,
        shipping_address_line2=shipping_address2,
        shipping_city=shipping_city,
        shipping_state=shipping_state,
        shipping_country=shipping_country,
        shipping_postal_code=shipping_postal,
    )
    
    # Create order items
    for item in cart:
        OrderItem.objects.create(
            order=order,
            product=item['product'],
            variant=item.get('variant'),
            product_name=item['product'].name,
            product_sku=item['product'].sku,
            variant_name=item.get('variant').name if item.get('variant') else '',
            quantity=item['quantity'],
            unit_price=item['price'],
            total_price=item['total_price'],
        )
        
        # Update product stock
        item['product'].stock -= item['quantity']
        item['product'].sales_count += item['quantity']
        item['product'].save()
    
    # Create status history
    OrderStatusHistory.objects.create(
        order=order,
        status='pending',
        note='Order created',
        created_by=request.user
    )
    
    # Clear cart
    cart.clear()
    
    # Send order confirmation email
    if send_order_confirmation_email(order):
        messages.success(request, f'Order {order.order_number} placed successfully! Check your email for confirmation.')
    else:
        messages.success(request, f'Order {order.order_number} placed successfully!')
    
    return redirect('orders:order_success', order_number=order.order_number)


@login_required
def order_success(request, order_number):
    """Order success page"""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, 'orders/order_success.html', {'order': order})
