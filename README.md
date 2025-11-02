# 🛍️ ShopHub E-Commerce Store

A **full-featured, professional e-commerce website** built with Django and Python. This project includes advanced features like user authentication, product catalog, shopping cart, checkout system, payment integration, product reviews, wishlists, and much more.

---

## ✨ Features

### 🔐 **Authentication System**
- User registration and login
- Email-based password reset
- User profiles with personal information
- Multiple shipping addresses management
- Order history and tracking
- Newsletter subscription

### 🛒 **Product Catalog**
- Categories with hierarchical support
- Brand management
- Product variants (size, color, etc.)
- Product specifications
- Multiple product images
- Stock management and inventory tracking
- Featured and new products
- Product search and filtering
- Price comparison and discount display
- Average ratings and reviews count

### 🛍️ **Shopping Experience**
- Session-based shopping cart
- Wishlist functionality
- Add to cart from product pages
- Update quantities in cart
- Real-time cart total calculation
- Guest checkout support

### 💳 **Checkout & Orders**
- Multi-step checkout process
- Shipping address selection
- Order summary and confirmation
- Order number generation
- Order status tracking (Pending, Processing, Shipped, Delivered, Cancelled)
- Payment status tracking
- Order history with detailed views

### ⭐ **Reviews & Ratings**
- Product reviews and ratings (1-5 stars)
- Verified purchase badges
- Helpful/not helpful votes on reviews
- Review images support
- Review moderation system

### 💰 **Payment Integration**
- Stripe payment gateway ready (configuration needed)
- Multiple payment methods support
- Payment confirmation and tracking
- Refund management system

### 🎨 **Modern UI/UX**
- Responsive Bootstrap 5 design
- Mobile-friendly interface
- Product cards with hover effects
- Discount badges and labels
- Search functionality
- Category browsing
- Hero section with call-to-action
- Features section showcasing benefits

### 👨‍💼 **Admin Dashboard**
- Custom Django admin interface
- Product management with inline editing
- Order management with status updates
- Customer management
- Review moderation
- Inventory tracking
- Sales reports (extensible)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ installed
- pip package manager

### Installation & Setup

1. **Navigate to the project directory:**
   ```bash
   cd D:/OneDrive/Desktop/django/ecommerce_store
   ```

2. **The database is already set up with migrations applied**

3. **Load sample data (already done):**
   ```bash
   /d/python/python manage.py load_sample_data
   ```

4. **Run the development server:**
   ```bash
   /d/python/python manage.py runserver
   ```

5. **Access the website:**
   - **Homepage:** http://127.0.0.1:8000/
   - **Admin Panel:** have password and gmail login



---

## 📦 Project Structure

```
ecommerce_store/
├── accounts/           # User authentication and profiles
│   ├── models.py      # Custom User model, Address
│   ├── views.py       # Login, register, profile views
│   ├── forms.py       # User forms
│   └── urls.py        # Authentication URLs
├── products/          # Product catalog
│   ├── models.py      # Product, Category, Brand, Variant
│   ├── views.py       # Product listing, detail, search
│   ├── urls.py        # Product URLs
│   └── admin.py       # Admin configuration
├── cart/              # Shopping cart
│   ├── cart.py        # Cart session management
│   ├── views.py       # Cart operations
│   ├── context_processors.py  # Cart context
│   └── urls.py        # Cart URLs
├── orders/            # Order management
│   ├── models.py      # Order, OrderItem, StatusHistory
│   ├── views.py       # Checkout, order creation
│   └── urls.py        # Order URLs
├── payments/          # Payment processing
│   ├── models.py      # Payment, Refund
│   └── admin.py       # Payment admin
├── reviews/           # Product reviews
│   ├── models.py      # Review, ReviewImage, ReviewVote
│   ├── forms.py       # Review forms
│   └── admin.py       # Review moderation
├── wishlist/          # Wishlist functionality
│   ├── models.py      # Wishlist, WishlistItem
│   ├── views.py       # Wishlist operations
│   └── urls.py        # Wishlist URLs
├── templates/         # HTML templates
│   ├── base.html      # Base template
│   ├── products/      # Product templates
│   ├── accounts/      # Auth templates
│   ├── cart/          # Cart templates
│   └── orders/        # Order templates
├── static/            # Static files (CSS, JS, images)
├── media/             # User-uploaded files
└── manage.py          # Django management script
```

---

## 🎯 Key Features Explained

### 1. **Custom User Model**
Extended Django's built-in User model with additional fields:
- Phone number
- Profile picture
- Date of birth
- Default address
- Newsletter subscription preference

### 2. **Advanced Product System**
- **Categories:** Hierarchical categories with parent-child relationships
- **Brands:** Brand management with logos and descriptions
- **Variants:** Product variations (e.g., size, color) with separate SKUs and pricing
- **Specifications:** Technical specifications for products
- **Multiple Images:** Main image + gallery images
- **SEO:** Meta titles and descriptions for better search engine optimization

### 3. **Smart Shopping Cart**
- Session-based cart (works without login)
- Persistent cart for logged-in users
- Automatic price calculation with variants
- Stock validation
- Easy quantity updates

### 4. **Comprehensive Order System**
- Unique order numbers (e.g., ORD-A1B2C3D4E5F6)
- Multiple order statuses with history tracking
- Shipping and billing addresses
- Tax and shipping calculations
- Order notes (customer and admin)
- Tracking number integration

### 5. **Review System**
- Star ratings (1-5 stars)
- Title and detailed comment
- Verified purchase badges
- Image uploads for reviews
- Community voting (helpful/not helpful)
- Admin moderation

---

## 🔧 Configuration

### Payment Gateway (Stripe)
To enable Stripe payments, update `ecommerce_store/settings.py`:

```python
STRIPE_PUBLIC_KEY = 'your-stripe-publishable-key'
STRIPE_SECRET_KEY = 'your-stripe-secret-key'
STRIPE_WEBHOOK_SECRET = 'your-stripe-webhook-secret'
```

### Email Settings
For production, configure email backend in `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

### Media Files
Product images and user uploads are stored in the `media/` directory. Make sure to configure your web server to serve these files in production.

---

## 🎨 Customization

### Change Theme Colors
Edit `templates/base.html` CSS variables:

```css
:root {
    --primary-color: #2563eb;      /* Primary brand color */
    --secondary-color: #64748b;    /* Secondary color */
    --accent-color: #f59e0b;       /* Accent/highlight color */
}
```

### Add More Products
Use the admin panel or create a custom management command:

```bash
/d/python/python manage.py load_sample_data
```

---

## 📱 Screenshots

The website includes:
- 🏠 **Homepage** with hero section, featured products, categories
- 🛍️ **Product Listing** with filters, search, and pagination
- 📦 **Product Detail** pages with images, descriptions, reviews
- 🛒 **Shopping Cart** with quantity management
- 💳 **Checkout** with address selection
- 👤 **User Dashboard** with orders, addresses, profile
- ⭐ **Review System** for customer feedback

---

## 🚀 Deployment Tips

### For Production:
1. Set `DEBUG = False` in `settings.py`
2. Configure allowed hosts: `ALLOWED_HOSTS = ['yourdomain.com']`
3. Use environment variables for sensitive data
4. Set up a proper database (PostgreSQL recommended)
5. Configure static files serving
6. Use a production web server (Gunicorn + Nginx)
7. Enable HTTPS/SSL
8. Set up email backend for notifications
9. Configure payment gateway properly

---

## 🛠️ Tech Stack

- **Backend:** Django 5.2.7
- **Frontend:** Bootstrap 5.3, Bootstrap Icons, Custom CSS with Gradients & Animations
- **Database:** SQLite (optimized for small to medium e-commerce sites)
- **Payment:** Stripe (ready for integration)
- **Images:** Pillow for image processing, Unsplash API for sample images
- **Session Management:** Django sessions for cart
- **Email System:** Order confirmations, shipping notifications, delivery confirmations
- **Currency:** Pakistani Rupee (PKR)

### Why SQLite?
SQLite is an excellent choice for your e-commerce store because:
- ✅ **Zero Configuration** - No database server setup required
- ✅ **High Performance** - Faster than client-server databases for small to medium sites
- ✅ **Reliable** - Used by billions of devices worldwide
- ✅ **Scalable** - Handles thousands of products and orders efficiently
- ✅ **Simple Backup** - Just copy the db.sqlite3 file
- ✅ **Perfect for** - Startups, small businesses, and sites with < 100,000 daily visitors

*Note: For enterprise-level scaling (millions of products/users), consider PostgreSQL migration later.*

---

## 📈 Future Enhancements

Potential features to add:
- [x] ✅ Email notifications for orders (order confirmation, shipping, delivery)
- [x] ✅ Colorful, modern UI with gradients and animations
- [x] ✅ Product images from Unsplash
- [x] ✅ PKR currency support
- [x] ✅ Enhanced admin panels with bulk actions
- [ ] Coupon/discount codes system
- [ ] Social authentication (Google, Facebook)
- [ ] Product recommendations based on browsing history
- [ ] Advanced analytics dashboard
- [ ] Multi-currency support
- [ ] Live chat support
- [ ] Product comparison feature
- [ ] Gift cards and vouchers
- [ ] Seller/vendor system for marketplace
- [ ] Mobile apps (React Native or Flutter)
- [ ] PostgreSQL migration for enterprise scaling

---

## 🤝 Contributing

This is a complete, production-ready e-commerce system. Feel free to customize it for your specific needs!

---

## 📝 License

This project is open-source and available for personal and commercial use.

---

## 🙋 Support

For admin access:
------have it but confidential

For shopping:
- **URL:** http://127.0.0.1:8000/

---

## ⚡ Quick Commands Reference

```bash
# Run development server
/d/python/python manage.py runserver

# Create superuser
/d/python/python manage.py createsuperuser

# Make migrations
/d/python/python manage.py makemigrations

# Apply migrations
/d/python/python manage.py migrate

# Load sample data
/d/python/python manage.py load_sample_data

# Create an app
/d/python/python manage.py startapp app_name

# Collect static files (for production)
/d/python/python manage.py collectstatic
```

---

**Built with ❤️ using Django & Python**

🎉 **Your professional e-commerce store is ready to use!**
# ecommerce-store
