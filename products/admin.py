from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Brand, Product, ProductImage, ProductVariant, ProductSpecification


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" style="object-fit: cover;" />', obj.image.url)
        return "No image"
    image_preview.short_description = 'Preview'


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1


class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'product_count', 'is_active', 'created_at']
    list_filter = ['is_active', 'parent', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active']
    actions = ['mark_as_active', 'mark_as_inactive']
    
    def product_count(self, obj):
        count = obj.products.count()
        return format_html('<strong>{}</strong> products', count)
    product_count.short_description = 'Products'
    
    def mark_as_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} categories marked as active.')
    mark_as_active.short_description = 'Mark selected as Active'
    
    def mark_as_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} categories marked as inactive.')
    mark_as_inactive.short_description = 'Mark selected as Inactive'


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'product_count', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active']
    actions = ['mark_as_active', 'mark_as_inactive']
    
    def product_count(self, obj):
        count = obj.products.count()
        return format_html('<strong>{}</strong> products', count)
    product_count.short_description = 'Products'
    
    def mark_as_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} brands marked as active.')
    mark_as_active.short_description = 'Mark selected as Active'
    
    def mark_as_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} brands marked as inactive.')
    mark_as_inactive.short_description = 'Mark selected as Inactive'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['image_preview', 'name', 'category', 'brand', 'price_display', 'stock_status', 'is_featured', 'is_active', 'created_at']
    list_filter = ['is_active', 'is_featured', 'is_new', 'category', 'brand', 'created_at']
    search_fields = ['name', 'description', 'sku']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_featured', 'is_active']
    inlines = [ProductImageInline, ProductVariantInline, ProductSpecificationInline]
    readonly_fields = ['image_preview', 'views', 'sales_count', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    actions = ['mark_as_featured', 'mark_as_active', 'mark_as_inactive', 'duplicate_products']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'slug', 'description', 'short_description')
        }),
        ('Categorization', {
            'fields': ('category', 'brand')
        }),
        ('Pricing', {
            'fields': ('price', 'compare_price', 'cost_price')
        }),
        ('Inventory', {
            'fields': ('sku', 'stock', 'low_stock_threshold')
        }),
        ('Product Details', {
            'fields': ('weight', 'dimensions', 'main_image', 'image_preview')
        }),
        ('Features', {
            'fields': ('is_featured', 'is_new', 'is_active')
        }),
        ('Statistics', {
            'fields': ('views', 'sales_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.main_image:
            return format_html('<img src="{}" width="100" height="100" style="object-fit: cover; border-radius: 5px;" />', obj.main_image.url)
        return "No image"
    image_preview.short_description = 'Image'
    
    def price_display(self, obj):
        if obj.compare_price and obj.compare_price > obj.price:
            return format_html(
                '<span style="color: red; font-weight: bold;">PKR {}</span><br/>'
                '<span style="text-decoration: line-through; color: gray;">PKR {}</span>',
                obj.price, obj.compare_price
            )
        return format_html('<span style="font-weight: bold;">PKR {}</span>', obj.price)
    price_display.short_description = 'Price'
    
    def stock_status(self, obj):
        if obj.stock <= 0:
            return format_html('<span style="color: red; font-weight: bold;">Out of Stock</span>')
        elif obj.stock <= obj.low_stock_threshold:
            return format_html('<span style="color: orange; font-weight: bold;">{} (Low Stock)</span>', obj.stock)
        return format_html('<span style="color: green; font-weight: bold;">{}</span>', obj.stock)
    stock_status.short_description = 'Stock'
    
    def mark_as_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} products marked as featured.')
    mark_as_featured.short_description = 'Mark selected as Featured'
    
    def mark_as_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} products marked as active.')
    mark_as_active.short_description = 'Mark selected as Active'
    
    def mark_as_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} products marked as inactive.')
    mark_as_inactive.short_description = 'Mark selected as Inactive'
    
    def duplicate_products(self, request, queryset):
        for product in queryset:
            product.pk = None
            product.name = f"{product.name} (Copy)"
            product.sku = f"{product.sku}-copy"
            product.slug = f"{product.slug}-copy"
            product.save()
        self.message_user(request, f'{queryset.count()} products duplicated.')
    duplicate_products.short_description = 'Duplicate selected products'
