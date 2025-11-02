from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.conf import settings


class Category(models.Model):
    """Product categories with hierarchy support"""
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']


class Brand(models.Model):
    """Product brands"""
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='brands/', blank=True, null=True)
    website = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class Product(models.Model):
    """Main product model with all features"""
    # Basic info
    name = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=500, blank=True)
    
    # Categorization
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    
    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2)
    compare_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Original price for discount display")
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Inventory
    sku = models.CharField(max_length=100, unique=True)
    stock = models.IntegerField(default=0)
    low_stock_threshold = models.IntegerField(default=10)
    
    # Product details
    weight = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, help_text="Weight in kg")
    dimensions = models.CharField(max_length=100, blank=True, help_text="L x W x H in cm")
    
    # Media
    main_image = models.ImageField(upload_to='products/')
    
    # Features
    is_featured = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # SEO
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    
    # Stats
    views = models.IntegerField(default=0)
    sales_count = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('products:product_detail', args=[self.slug])
    
    @property
    def discount_percentage(self):
        if self.compare_price:
            return int(((self.compare_price - self.price) / self.compare_price) * 100)
        return 0
    
    @property
    def is_in_stock(self):
        return self.stock > 0
    
    @property
    def is_low_stock(self):
        return self.stock <= self.low_stock_threshold
    
    @property
    def average_rating(self):
        reviews = self.reviews.filter(is_approved=True)
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return 0
    
    @property
    def reviews_count(self):
        return self.reviews.filter(is_approved=True).count()
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['-created_at']),
        ]


class ProductImage(models.Model):
    """Additional product images"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.product.name} - Image {self.order}"
    
    class Meta:
        ordering = ['order']


class ProductVariant(models.Model):
    """Product variants (size, color, etc.)"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    name = models.CharField(max_length=100, help_text="e.g., Size, Color")
    value = models.CharField(max_length=100, help_text="e.g., Large, Red")
    sku = models.CharField(max_length=100, unique=True)
    price_adjustment = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Additional price for this variant")
    stock = models.IntegerField(default=0)
    image = models.ImageField(upload_to='variants/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.product.name} - {self.name}: {self.value}"
    
    class Meta:
        unique_together = ['product', 'name', 'value']


class ProductSpecification(models.Model):
    """Technical specifications for products"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='specifications')
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=300)
    order = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.product.name} - {self.name}"
    
    class Meta:
        ordering = ['order']
