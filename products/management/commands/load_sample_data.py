from django.core.management.base import BaseCommand
from products.models import Category, Brand, Product
from decimal import Decimal
from django.core.files.base import ContentFile
import urllib.request


class Command(BaseCommand):
    help = 'Load sample products into the database'

    def download_image(self, url, name):
        """Download image from URL"""
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                return ContentFile(response.read(), name=name)
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Could not download image: {e}'))
            return None

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample data...')
        
        # Clear existing data
        Product.objects.all().delete()
        Category.objects.all().delete()
        Brand.objects.all().delete()
        
        # Create categories with placeholder images
        electronics = Category.objects.create(
            name='Electronics',
            slug='electronics',
            description='Latest electronic gadgets and devices'
        )
        
        clothing = Category.objects.create(
            name='Clothing',
            slug='clothing',
            description='Fashion and apparel for everyone'
        )
        
        shoes = Category.objects.create(
            name='Shoes',
            slug='shoes',
            description='Footwear for all occasions'
        )
        
        accessories = Category.objects.create(
            name='Accessories',
            slug='accessories',
            description='Style your look with our accessories'
        )
        
        self.stdout.write(self.style.SUCCESS('✓ Created categories'))
        
        # Create brands
        nike = Brand.objects.create(name='Nike', slug='nike', description='Just Do It')
        adidas = Brand.objects.create(name='Adidas', slug='adidas', description='Impossible is Nothing')
        apple = Brand.objects.create(name='Apple', slug='apple', description='Think Different')
        samsung = Brand.objects.create(name='Samsung', slug='samsung', description='Do What You Cant')
        
        self.stdout.write(self.style.SUCCESS('✓ Created brands'))
        
        # Placeholder image URLs from Unsplash (free to use)
        product_images = {
            'shoes1': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500',  # Nike shoes
            'shoes2': 'https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=500',  # Adidas shoes
            'phone1': 'https://images.unsplash.com/photo-1592286927505-038c78d7f788?w=500',  # iPhone
            'phone2': 'https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=500',  # Samsung phone
            'hoodie': 'https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=500',   # Hoodie
            'tshirt': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500',  # T-shirt
            'airpods': 'https://images.unsplash.com/photo-1606841837239-c5a1a4a07af7?w=500', # AirPods
            'watch': 'https://images.unsplash.com/photo-1579586337278-3befd40fd17a?w=500',  # Smartwatch
        }
        
        # Create products
        products = [
            {
                'name': 'Nike Air Max 2024',
                'slug': 'nike-air-max-2024',
                'description': 'Experience ultimate comfort and style with the Nike Air Max 2024. Features innovative cushioning technology and breathable mesh upper. Perfect for running, walking, or casual wear.',
                'short_description': 'Premium running shoes with Air Max cushioning',
                'category': shoes,
                'brand': nike,
                'price': Decimal('149.99'),
                'compare_price': Decimal('199.99'),
                'sku': 'NIKE-AM-2024',
                'stock': 50,
                'is_featured': True,
                'is_new': True,
                'image_key': 'shoes1'
            },
            {
                'name': 'Adidas Ultraboost 22',
                'slug': 'adidas-ultraboost-22',
                'description': 'The Adidas Ultraboost 22 delivers energy-returning cushioning for your everyday runs. Engineered for comfort and performance with a Continental rubber outsole.',
                'short_description': 'Energy-returning running shoes',
                'category': shoes,
                'brand': adidas,
                'price': Decimal('139.99'),
                'compare_price': Decimal('180.00'),
                'sku': 'ADIDAS-UB-22',
                'stock': 40,
                'is_featured': True,
                'image_key': 'shoes2'
            },
            {
                'name': 'Apple iPhone 15 Pro',
                'slug': 'apple-iphone-15-pro',
                'description': 'The most powerful iPhone ever. Features A17 Pro chip, titanium design, and advanced camera system with 48MP main camera. 5G enabled with all-day battery life.',
                'short_description': 'Latest iPhone with titanium design',
                'category': electronics,
                'brand': apple,
                'price': Decimal('999.00'),
                'compare_price': Decimal('1099.00'),
                'sku': 'APPLE-IP15P',
                'stock': 30,
                'is_featured': True,
                'is_new': True,
                'image_key': 'phone1'
            },
            {
                'name': 'Samsung Galaxy S24 Ultra',
                'slug': 'samsung-galaxy-s24-ultra',
                'description': 'Epic in every way. Galaxy AI is here. 200MP camera, S Pen included, and long-lasting battery. 6.8" Dynamic AMOLED display with 120Hz refresh rate.',
                'short_description': 'Flagship Android phone with S Pen',
                'category': electronics,
                'brand': samsung,
                'price': Decimal('1199.00'),
                'sku': 'SAMSUNG-S24U',
                'stock': 25,
                'is_featured': True,
                'image_key': 'phone2'
            },
            {
                'name': 'Nike Sportswear Tech Fleece Hoodie',
                'slug': 'nike-tech-fleece-hoodie',
                'description': 'Stay warm and comfortable in the Nike Tech Fleece Hoodie. Premium fleece fabric with modern design. Features zippered pockets and adjustable hood.',
                'short_description': 'Premium fleece hoodie',
                'category': clothing,
                'brand': nike,
                'price': Decimal('89.99'),
                'compare_price': Decimal('120.00'),
                'sku': 'NIKE-TF-HOOD',
                'stock': 60,
                'is_new': True,
                'image_key': 'hoodie'
            },
            {
                'name': 'Adidas Originals Trefoil T-Shirt',
                'slug': 'adidas-trefoil-tshirt',
                'description': 'Classic Adidas style with the iconic Trefoil logo. Made from soft cotton for everyday wear. Available in multiple colors and sizes.',
                'short_description': 'Classic Adidas t-shirt',
                'category': clothing,
                'brand': adidas,
                'price': Decimal('29.99'),
                'sku': 'ADIDAS-TF-TEE',
                'stock': 100,
                'image_key': 'tshirt'
            },
            {
                'name': 'Apple AirPods Pro (2nd Gen)',
                'slug': 'apple-airpods-pro-2',
                'description': 'Active Noise Cancellation, Transparency mode, and personalized Spatial Audio. Up to 6 hours of listening time. Wireless charging case included.',
                'short_description': 'Premium wireless earbuds',
                'category': electronics,
                'brand': apple,
                'price': Decimal('249.00'),
                'sku': 'APPLE-APP2',
                'stock': 45,
                'is_featured': True,
                'image_key': 'airpods'
            },
            {
                'name': 'Samsung Galaxy Watch 6',
                'slug': 'samsung-galaxy-watch-6',
                'description': 'Advanced health tracking, personalized HR Zone, and sleep tracking. Perfect companion for your active lifestyle. Water resistant up to 5ATM.',
                'short_description': 'Smart fitness watch',
                'category': accessories,
                'brand': samsung,
                'price': Decimal('299.00'),
                'compare_price': Decimal('349.00'),
                'sku': 'SAMSUNG-GW6',
                'stock': 35,
                'is_new': True,
                'image_key': 'watch'
            },
        ]
        
        for product_data in products:
            image_key = product_data.pop('image_key')
            image_url = product_images.get(image_key)
            
            product = Product.objects.create(**product_data)
            
            # Try to download and attach image
            if image_url:
                image_file = self.download_image(image_url, f'{product.slug}.jpg')
                if image_file:
                    product.main_image.save(f'{product.slug}.jpg', image_file, save=True)
                    self.stdout.write(self.style.SUCCESS(f'  ✓ Added image for {product.name}'))
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(products)} products'))
        self.stdout.write(self.style.SUCCESS('\n✨ Sample data loaded successfully with images!'))
