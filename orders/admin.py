from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import Order, OrderItem, OrderStatusHistory
from .emails import send_order_shipped_email, send_order_delivered_email


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'variant', 'product_name', 'product_sku', 'variant_name', 'quantity', 'unit_price', 'total_price']
    can_delete = False


class OrderStatusHistoryInline(admin.TabularInline):
    model = OrderStatusHistory
    extra = 1
    readonly_fields = ['created_at', 'created_by']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user_link', 'status_badge', 'payment_status_badge', 'total_display', 'items_count', 'created_at']
    list_filter = ['status', 'payment_status', 'created_at', 'updated_at']
    search_fields = ['order_number', 'user__username', 'user__email', 'shipping_full_name', 'shipping_phone']
    readonly_fields = ['order_number', 'created_at', 'updated_at', 'paid_at', 'shipped_at', 'delivered_at']
    inlines = [OrderItemInline, OrderStatusHistoryInline]
    date_hierarchy = 'created_at'
    list_per_page = 25
    actions = ['mark_as_processing', 'mark_as_shipped', 'mark_as_delivered', 'mark_as_paid']
    
    fieldsets = (
        ('Order Info', {
            'fields': ('order_number', 'user', 'status', 'payment_status')
        }),
        ('Pricing', {
            'fields': ('subtotal', 'tax', 'shipping_cost', 'discount', 'total')
        }),
        ('Shipping Address', {
            'fields': ('shipping_full_name', 'shipping_phone', 'shipping_address_line1', 
                      'shipping_address_line2', 'shipping_city', 'shipping_state', 
                      'shipping_country', 'shipping_postal_code')
        }),
        ('Tracking', {
            'fields': ('tracking_number', 'carrier')
        }),
        ('Notes', {
            'fields': ('customer_notes', 'admin_notes'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'paid_at', 'shipped_at', 'delivered_at'),
            'classes': ('collapse',)
        }),
    )
    
    def user_link(self, obj):
        url = reverse('admin:accounts_user_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    user_link.short_description = 'Customer'
    
    def status_badge(self, obj):
        colors = {
            'pending': 'orange',
            'processing': 'blue',
            'shipped': 'purple',
            'delivered': 'green',
            'cancelled': 'red',
            'refunded': 'gray'
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-weight: bold;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def payment_status_badge(self, obj):
        colors = {
            'pending': 'orange',
            'completed': 'green',
            'failed': 'red',
            'refunded': 'gray'
        }
        color = colors.get(obj.payment_status, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color, obj.get_payment_status_display()
        )
    payment_status_badge.short_description = 'Payment'
    
    def total_display(self, obj):
        return format_html('<strong>PKR {}</strong>', obj.total)
    total_display.short_description = 'Total'
    
    def items_count(self, obj):
        return obj.items.count()
    items_count.short_description = 'Items'
    
    def mark_as_processing(self, request, queryset):
        updated = queryset.update(status='processing')
        for order in queryset:
            OrderStatusHistory.objects.create(
                order=order,
                status='processing',
                note='Status updated by admin',
                created_by=request.user
            )
        self.message_user(request, f'{updated} orders marked as processing.')
    mark_as_processing.short_description = 'Mark as Processing'
    
    def mark_as_shipped(self, request, queryset):
        now = timezone.now()
        updated = queryset.update(status='shipped', shipped_at=now)
        for order in queryset:
            OrderStatusHistory.objects.create(
                order=order,
                status='shipped',
                note='Order shipped by admin',
                created_by=request.user
            )
            # Send shipping notification email
            send_order_shipped_email(order)
        self.message_user(request, f'{updated} orders marked as shipped and emails sent.')
    mark_as_shipped.short_description = 'Mark as Shipped (Sends Email)'
    
    def mark_as_delivered(self, request, queryset):
        now = timezone.now()
        updated = queryset.update(status='delivered', delivered_at=now)
        for order in queryset:
            OrderStatusHistory.objects.create(
                order=order,
                status='delivered',
                note='Order delivered',
                created_by=request.user
            )
            # Send delivery confirmation email
            send_order_delivered_email(order)
        self.message_user(request, f'{updated} orders marked as delivered and emails sent.')
    mark_as_delivered.short_description = 'Mark as Delivered (Sends Email)'
    
    def mark_as_paid(self, request, queryset):
        now = timezone.now()
        updated = queryset.update(payment_status='completed', paid_at=now)
        self.message_user(request, f'{updated} orders marked as paid.')
    mark_as_paid.short_description = 'Mark as Paid'
