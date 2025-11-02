from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q, Avg, Count
from django.contrib import messages
from .models import Product, Category, Brand
from reviews.models import Review
from reviews.forms import ReviewForm


def home(request):
    """Homepage with featured and new products"""
    featured_products = Product.objects.filter(is_featured=True, is_active=True)[:8]
    new_products = Product.objects.filter(is_new=True, is_active=True)[:8]
    categories = Category.objects.filter(is_active=True, parent=None)[:6]
    
    context = {
        'featured_products': featured_products,
        'new_products': new_products,
        'categories': categories,
    }
    return render(request, 'products/home.html', context)


def product_list(request):
    """Product catalog with filters and search"""
    products = Product.objects.filter(is_active=True)
    
    # Search
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(brand__name__icontains=query) |
            Q(category__name__icontains=query)
        )
    
    # Category filter
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # Brand filter
    brand_slug = request.GET.get('brand')
    if brand_slug:
        brand = get_object_or_404(Brand, slug=brand_slug)
        products = products.filter(brand=brand)
    
    # Price range filter
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    
    # Sorting
    sort = request.GET.get('sort', '-created_at')
    if sort == 'price_low':
        products = products.order_by('price')
    elif sort == 'price_high':
        products = products.order_by('-price')
    elif sort == 'name':
        products = products.order_by('name')
    elif sort == 'popular':
        products = products.order_by('-sales_count')
    else:
        products = products.order_by(sort)
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all categories and brands for filters
    categories = Category.objects.filter(is_active=True)
    brands = Brand.objects.filter(is_active=True)
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'brands': brands,
        'query': query,
        'current_sort': sort,
    }
    return render(request, 'products/product_list.html', context)


def product_detail(request, slug):
    """Product detail page with reviews"""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    
    # Increment views
    product.views += 1
    product.save(update_fields=['views'])
    
    # Get related products
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id)[:4]
    
    # Get reviews
    reviews = Review.objects.filter(product=product, is_approved=True).select_related('user')
    
    # Review form (if user is logged in)
    review_form = None
    user_review = None
    if request.user.is_authenticated:
        # Check if user already reviewed this product
        user_review = Review.objects.filter(product=product, user=request.user).first()
        
        if request.method == 'POST' and not user_review:
            review_form = ReviewForm(request.POST, request.FILES)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.product = product
                review.user = request.user
                review.save()
                messages.success(request, 'Thank you for your review!')
                return redirect('products:product_detail', slug=slug)
        elif not user_review:
            review_form = ReviewForm()
    
    context = {
        'product': product,
        'related_products': related_products,
        'reviews': reviews,
        'review_form': review_form,
        'user_review': user_review,
    }
    return render(request, 'products/product_detail.html', context)


def category_detail(request, slug):
    """Category page"""
    category = get_object_or_404(Category, slug=slug, is_active=True)
    products = Product.objects.filter(category=category, is_active=True)
    
    # Sorting
    sort = request.GET.get('sort', '-created_at')
    if sort == 'price_low':
        products = products.order_by('price')
    elif sort == 'price_high':
        products = products.order_by('-price')
    elif sort == 'name':
        products = products.order_by('name')
    else:
        products = products.order_by(sort)
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'products': page_obj,
        'page_obj': page_obj,
        'current_sort': sort,
    }
    return render(request, 'products/category_detail.html', context)


def brand_detail(request, slug):
    """Brand page"""
    brand = get_object_or_404(Brand, slug=slug, is_active=True)
    products = Product.objects.filter(brand=brand, is_active=True)
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'brand': brand,
        'products': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'products/brand_detail.html', context)


def search(request):
    """Advanced search page"""
    query = request.GET.get('q', '')
    products = Product.objects.filter(is_active=True)
    
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(brand__name__icontains=query) |
            Q(category__name__icontains=query) |
            Q(sku__icontains=query)
        )
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'query': query,
        'products': page_obj,
        'page_obj': page_obj,
        'total_results': products.count(),
    }
    return render(request, 'products/search.html', context)
