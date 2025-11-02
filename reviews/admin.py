from django.contrib import admin
from django.utils.html import format_html
from .models import Review, ReviewImage, ReviewVote


class ReviewImageInline(admin.TabularInline):
    model = ReviewImage
    extra = 0
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="80" height="80" style="object-fit: cover;" />', obj.image.url)
        return "No image"
    image_preview.short_description = 'Preview'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product_link', 'user', 'rating_display', 'title', 'is_verified_purchase', 'is_approved', 'helpful_votes', 'created_at']
    list_filter = ['rating', 'is_verified_purchase', 'is_approved', 'created_at']
    search_fields = ['product__name', 'user__username', 'title', 'comment']
    list_editable = ['is_approved']
    inlines = [ReviewImageInline]
    date_hierarchy = 'created_at'
    actions = ['approve_reviews', 'unapprove_reviews']
    readonly_fields = ['created_at', 'updated_at']
    
    def product_link(self, obj):
        return format_html('<a href="/product/{}">{}</a>', obj.product.slug, obj.product.name)
    product_link.short_description = 'Product'
    
    def rating_display(self, obj):
        stars = '⭐' * obj.rating
        color = 'green' if obj.rating >= 4 else 'orange' if obj.rating >= 3 else 'red'
        return format_html('<span style="color: {};">{} ({})</span>', color, stars, obj.rating)
    rating_display.short_description = 'Rating'
    
    def helpful_votes(self, obj):
        helpful = obj.votes.filter(is_helpful=True).count()
        not_helpful = obj.votes.filter(is_helpful=False).count()
        return format_html('👍 {} / 👎 {}', helpful, not_helpful)
    helpful_votes.short_description = 'Votes'
    
    def approve_reviews(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} reviews approved.')
    approve_reviews.short_description = 'Approve selected reviews'
    
    def unapprove_reviews(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} reviews unapproved.')
    unapprove_reviews.short_description = 'Unapprove selected reviews'
