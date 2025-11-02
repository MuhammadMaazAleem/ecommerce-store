from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, Address


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'full_name_display', 'orders_count', 'is_staff', 'is_active', 'created_at']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'newsletter_subscribed', 'created_at']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'phone']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    actions = ['activate_users', 'deactivate_users', 'subscribe_newsletter']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone', 'date_of_birth', 'profile_picture')}),
        ('Address', {'fields': ('address_line1', 'address_line2', 'city', 'state', 'country', 'postal_code')}),
        ('Preferences', {'fields': ('newsletter_subscribed',)}),
    )
    
    def full_name_display(self, obj):
        return obj.get_full_name() or '-'
    full_name_display.short_description = 'Full Name'
    
    def orders_count(self, obj):
        count = obj.orders.count()
        if count > 0:
            return format_html('<strong style="color: green;">{}</strong> orders', count)
        return '0 orders'
    orders_count.short_description = 'Orders'
    
    def activate_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} users activated.')
    activate_users.short_description = 'Activate selected users'
    
    def deactivate_users(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} users deactivated.')
    deactivate_users.short_description = 'Deactivate selected users'
    
    def subscribe_newsletter(self, request, queryset):
        updated = queryset.update(newsletter_subscribed=True)
        self.message_user(request, f'{updated} users subscribed to newsletter.')
    subscribe_newsletter.short_description = 'Subscribe to newsletter'


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'user', 'address_preview', 'city', 'country', 'is_default', 'created_at']
    list_filter = ['is_default', 'country', 'created_at']
    search_fields = ['full_name', 'user__username', 'city', 'postal_code', 'phone']
    ordering = ['-created_at']
    
    def address_preview(self, obj):
        return f"{obj.address_line1}, {obj.city}"
    address_preview.short_description = 'Address'
