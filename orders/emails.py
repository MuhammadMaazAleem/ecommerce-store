from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


def send_order_confirmation_email(order):
    """Send order confirmation email"""
    try:
        subject = f'Order Confirmation - {order.order_number}'
        
        # Plain text
        plain_message = f"""
Dear {order.shipping_full_name},

Thank you for your order!

Order Number: {order.order_number}
Order Date: {order.created_at.strftime('%B %d, %Y')}
Total Amount: PKR {order.total}

We'll send you another email when your order ships.

Thank you for shopping with ShopHub!
"""
        
        # HTML
        html_message = render_to_string('emails/order_confirmation.html', {'order': order})
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.user.email],
            html_message=html_message,
            fail_silently=True,
        )
        return True
    except Exception as e:
        print(f"❌ Order confirmation email failed: {e}")
        return False


def send_order_shipped_email(order):
    """Send order shipped notification email"""
    try:
        subject = f'Your Order Has Shipped - {order.order_number}'
        
        # Plain text
        plain_message = f"""
Dear {order.shipping_full_name},

Great news! Your order has been shipped.

Order Number: {order.order_number}
Tracking Number: {order.tracking_number if order.tracking_number else 'Will be updated soon'}
Carrier: {order.carrier if order.carrier else 'Standard Shipping'}

Your package is on its way and should arrive within 3-5 business days.

Track your order: http://127.0.0.1:8000/accounts/orders/

Thank you for shopping with ShopHub!
"""
        
        # HTML
        html_message = render_to_string('emails/order_shipped.html', {'order': order})
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.user.email],
            html_message=html_message,
            fail_silently=True,
        )
        print(f"✅ Shipping notification sent to {order.user.email}")
        return True
    except Exception as e:
        print(f"❌ Shipping notification failed: {e}")
        return False


def send_order_delivered_email(order):
    """Send order delivered notification email"""
    try:
        subject = f'Order Delivered - {order.order_number}'
        
        # Plain text
        plain_message = f"""
Dear {order.shipping_full_name},

Your order has been successfully delivered!

Order Number: {order.order_number}
Delivered On: {order.delivered_at.strftime('%B %d, %Y')}

We hope you love your purchase! Please consider leaving a review.

Thank you for shopping with ShopHub!
"""
        
        # HTML
        html_message = render_to_string('emails/order_delivered.html', {'order': order})
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.user.email],
            html_message=html_message,
            fail_silently=True,
        )
        print(f"✅ Delivery confirmation sent to {order.user.email}")
        return True
    except Exception as e:
        print(f"❌ Delivery notification failed: {e}")
        return False
