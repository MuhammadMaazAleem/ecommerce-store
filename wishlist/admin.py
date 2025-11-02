from django.contrib import admin
from django.utils.html import format_html
from .models import Wishlist, WishlistItem


class WishlistItemInline(admin.TabularInline):
    model = WishlistItem
    extra = 0
    readonly_fields = ['product_preview', 'added_at']
    
    def product_preview(self, obj):
        if obj.product.main_image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover;"/> {}',
                obj.product.main_image.url, obj.product.name
            )
        return obj.product.name
    product_preview.short_description = 'Product'


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'items_count', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at']
    inlines = [WishlistItemInline]
    
    def items_count(self, obj):
        count = obj.items.count()
        return format_html('<strong>{}</strong> items', count)
    items_count.short_description = 'Items'


@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ['wishlist_user', 'product', 'added_at']
    list_filter = ['added_at']
    search_fields = ['wishlist__user__username', 'product__name']
    readonly_fields = ['added_at']
    
    def wishlist_user(self, obj):
        return obj.wishlist.user.username
    wishlist_user.short_description = 'User'
