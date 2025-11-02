from django.contrib import admin
from django.utils.html import format_html
from .models import Payment, Refund


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['order_link', 'payment_method', 'status_badge', 'amount_display', 'transaction_id', 'created_at']
    list_filter = ['payment_method', 'status', 'created_at']
    search_fields = ['order__order_number', 'transaction_id', 'stripe_payment_intent_id']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Payment Info', {
            'fields': ('order', 'payment_method', 'status', 'amount', 'currency')
        }),
        ('Transaction Details', {
            'fields': ('transaction_id', 'stripe_payment_intent_id', 'stripe_charge_id')
        }),
        ('Metadata', {
            'fields': ('payment_details', 'failure_reason'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def order_link(self, obj):
        return format_html('<a href="/admin/orders/order/{}/change/">{}</a>', obj.order.id, obj.order.order_number)
    order_link.short_description = 'Order'
    
    def status_badge(self, obj):
        colors = {
            'pending': 'orange',
            'completed': 'green',
            'failed': 'red',
            'refunded': 'gray'
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def amount_display(self, obj):
        return format_html('<strong>PKR {}</strong>', obj.amount)
    amount_display.short_description = 'Amount'


@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ['payment_link', 'status_badge', 'amount_display', 'reason_preview', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['payment__order__order_number', 'payment__transaction_id', 'reason']
    readonly_fields = ['created_at', 'processed_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Refund Info', {
            'fields': ('payment', 'amount', 'status', 'reason')
        }),
        ('Processing', {
            'fields': ('refund_transaction_id', 'processed_by', 'processed_at')
        }),
        ('Admin Notes', {
            'fields': ('admin_notes',),
            'classes': ('collapse',)
        }),
    )
    
    def payment_link(self, obj):
        return format_html(
            '<a href="/admin/payments/payment/{}/change/">Payment #{}</a>',
            obj.payment.id, obj.payment.id
        )
    payment_link.short_description = 'Payment'
    
    def status_badge(self, obj):
        colors = {
            'pending': 'orange',
            'approved': 'blue',
            'completed': 'green',
            'rejected': 'red'
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def amount_display(self, obj):
        return format_html('<strong>PKR {}</strong>', obj.amount)
    amount_display.short_description = 'Amount'
    
    def reason_preview(self, obj):
        return obj.reason[:50] + '...' if len(obj.reason) > 50 else obj.reason
    reason_preview.short_description = 'Reason'
