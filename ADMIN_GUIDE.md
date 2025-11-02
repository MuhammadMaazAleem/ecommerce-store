# 🎯 ShopHub Admin Guide

## 🔐 Access Admin Panel
**URL:** http://127.0.0.1:8000/admin/

**Default Credentials:**
- Username: `admin`
- Password: `admin123`

---

## 📦 Product Management

### ➕ Add New Product
1. Navigate to **Products** → **Products** → **Add Product**
2. Fill in required fields:
   - **Name** (auto-generates slug)
   - **Category** & **Brand**
   - **Price** (in PKR)
   - **Stock quantity**
   - **Description**
3. Upload main image
4. Add additional images using "Product Images" inline
5. Mark as **Featured** or **New** if desired
6. Click **Save**

### ✏️ Edit Product
1. Go to **Products** → **Products**
2. Click on product name to edit
3. Modify any field (price, stock, description, images)
4. You can directly edit **Price**, **Stock**, **Featured**, and **Active** status from the list view
5. Click **Save**

### 🗑️ Delete Product
1. Select products using checkboxes
2. Choose "Delete selected products" from Actions dropdown
3. Confirm deletion

### 🎨 Bulk Actions on Products
- **Mark as Featured**: Highlight products on homepage
- **Mark as Active/Inactive**: Show/hide products from store
- **Duplicate Products**: Create copies for quick variants

### 💰 Change Product Price
**Method 1 - Quick Edit:**
1. Go to Products list
2. Change price directly in the list view
3. Scroll down and click "Save"

**Method 2 - Detailed Edit:**
1. Click product name
2. Go to "Pricing" section
3. Update:
   - **Price**: Current selling price
   - **Compare Price**: Original price (shows discount)
   - **Cost Price**: Your purchase cost
4. Save changes

### 📊 Product Features
- **Image Preview**: See product images in admin list
- **Stock Status**: Color-coded (Green=In Stock, Orange=Low, Red=Out)
- **Price Display**: Shows discount if compare price is set

---

## 📂 Category Management

### Add Category
1. Go to **Products** → **Categories** → **Add Category**
2. Enter name (slug auto-generated)
3. Select parent category (optional, for subcategories)
4. Add description
5. Mark as **Active**
6. Save

### Edit/Delete Categories
- Click category name to edit
- Use checkboxes + actions for bulk operations
- **Product Count** shows how many products in each category

---

## 🏷️ Brand Management

### Add Brand
1. **Products** → **Brands** → **Add Brand**
2. Fill name, description
3. Mark as active
4. Save

### Manage Brands
- View product count per brand
- Bulk activate/deactivate brands

---

## 📋 Order Management

### View Orders
- **Orders** → **Orders**
- See all orders with:
  - Order number
  - Customer name
  - Status (color-coded badges)
  - Payment status
  - Total amount in PKR

### Update Order Status
**Method 1 - Individual:**
1. Click order number
2. Change **Status** dropdown:
   - Pending
   - Processing
   - Shipped
   - Delivered
   - Cancelled
3. Add tracking number if shipped
4. Add admin notes
5. Save

**Method 2 - Bulk Actions:**
1. Select multiple orders
2. Choose action:
   - Mark as Processing
   - Mark as Shipped (sets shipped date)
   - Mark as Delivered (sets delivered date)
   - Mark as Paid (sets payment status)

### Order Details View
- View all items in order
- See shipping address
- Check payment status
- Add tracking information
- View status history

### 📦 Change Order Items
- Order items are **read-only** after creation
- To modify, you need to cancel and create new order

---

## 👥 Customer Management

### View Customers
- **Accounts** → **Users**
- See all registered users
- View order count per customer
- Filter by staff/active status

### Manage Customers
- **Activate/Deactivate** users
- Subscribe to newsletter
- View customer's orders
- Edit customer information

### Customer Addresses
- **Accounts** → **Addresses**
- View all saved addresses
- See which is default
- Edit or delete addresses

---

## ⭐ Review Management

### Moderate Reviews
1. **Reviews** → **Reviews**
2. View all product reviews with:
   - Star rating (color-coded)
   - Product name
   - Customer name
   - Verified purchase badge
3. Check **Is Approved** to publish review
4. Uncheck to hide from public

### Bulk Actions
- **Approve selected reviews**: Publish multiple reviews
- **Unapprove selected reviews**: Hide reviews

### Review Features
- See helpful votes (👍/👎)
- View review images inline
- Filter by rating, verified purchase, approval status

---

## 💳 Payment Management

### View Payments
- **Payments** → **Payments**
- See all transactions
- Status color-coded:
  - 🟠 Orange = Pending
  - 🟢 Green = Completed
  - 🔴 Red = Failed
  - ⚪ Gray = Refunded

### Process Refunds
1. **Payments** → **Refunds**
2. Create new refund or view existing
3. Change status:
   - Pending
   - Approved
   - Completed
   - Rejected
4. Add admin notes

---

## ❤️ Wishlist Management

### View Wishlists
- **Wishlists** → **Wishlists**
- See each user's wishlist
- View item count
- See products with images

---

## 🔍 Search & Filters

### Quick Search
- Use search bar at top of each section
- Searches across multiple fields (name, email, order number, etc.)

### Advanced Filters
- Right sidebar has filters:
  - Date ranges
  - Status
  - Categories/Brands
  - Active/Inactive
- Combine multiple filters

### Date Hierarchy
- Orders and Products have date drill-down
- Click year → month → day to filter

---

## 📊 Admin Dashboard Features

### Quick Stats
- Total products, orders, customers visible at a glance
- Color-coded status indicators
- Product stock alerts

### Inline Editing
- Edit product images without leaving product page
- Add variants and specifications inline
- Quick price/stock updates from list view

### Batch Operations
- Select multiple items with checkboxes
- Apply actions to all selected items
- Bulk update status, prices, visibility

---

## 🎯 Common Admin Tasks

### 1️⃣ Add Product with Images
```
Admin → Products → Add Product
→ Fill basic info
→ Upload main image
→ Scroll to "Product Images" section
→ Add multiple images
→ Save
```

### 2️⃣ Update Product Price
```
Admin → Products → Products List
→ Change price in the list
→ Scroll down → Click "Save"
```

### 3️⃣ Mark Order as Shipped
```
Admin → Orders → Select orders
→ Actions: "Mark as Shipped"
→ Or edit individually to add tracking number
```

### 4️⃣ Feature Products on Homepage
```
Admin → Products → Select products
→ Actions: "Mark selected as Featured"
→ Products appear in homepage "Featured" section
```

### 5️⃣ Approve Reviews
```
Admin → Reviews → Select reviews
→ Actions: "Approve selected reviews"
→ Or check "Is Approved" in list view
```

### 6️⃣ Add New Category
```
Admin → Products → Categories → Add Category
→ Enter name (slug auto-fills)
→ Select parent if subcategory
→ Mark as Active → Save
```

---

## ⚙️ Admin Features Summary

✅ **Product Management**
- Add/Edit/Delete products
- Bulk price updates
- Stock management
- Image galleries
- Product variants

✅ **Order Processing**
- View all orders
- Update order status
- Bulk status changes
- Add tracking numbers
- Order history tracking

✅ **Customer Management**
- View customer details
- See order history per customer
- Manage addresses
- Bulk user actions

✅ **Content Moderation**
- Approve/reject reviews
- Manage ratings
- View review images

✅ **Payment Tracking**
- View all transactions
- Process refunds
- Payment status updates

✅ **Inventory Control**
- Stock level monitoring
- Low stock alerts
- Product availability toggle

---

## 🚀 Tips & Best Practices

### 💡 Quick Tips
1. **Use Bulk Actions**: Save time by updating multiple items at once
2. **Use Filters**: Narrow down large lists quickly
3. **Check Stock Alerts**: Red/orange indicators show low stock
4. **Add Product Images**: Products with images sell better
5. **Approve Reviews**: Social proof increases sales
6. **Update Order Status**: Keep customers informed
7. **Use Featured Products**: Highlight bestsellers on homepage

### ⚠️ Important Notes
- Prices are in PKR (Pakistani Rupees)
- Orders create inventory snapshots (can't be edited after creation)
- Deactivating products hides them from store but keeps data
- Deleting categories doesn't delete products in them
- Review approval is required before public display

---

## 🆘 Need Help?

### Common Issues

**Q: Can't see newly added product on website?**
- A: Make sure "Is Active" is checked
- Check if product has stock > 0
- Verify category is active

**Q: How to create a sale/discount?**
- A: Set "Compare Price" higher than "Price"
- Discount percentage calculates automatically

**Q: Product images not showing?**
- A: Make sure images are uploaded as main_image
- Check MEDIA_URL settings

**Q: Can't edit order items?**
- A: Order items are locked after creation
- Cancel order and create new one if needed

---

## 📱 Admin Access Levels

### Superuser (Full Access)
- ✅ Add/Edit/Delete everything
- ✅ Access all sections
- ✅ Manage users and permissions

### Staff User (Limited Access)
- ✅ View orders
- ✅ Update order status
- ✅ Manage products
- ❌ Can't delete users
- ❌ Can't access settings

---

## 🎨 Admin Customization

**Current Theme:** ShopHub Administration  
**Dashboard Title:** "Welcome to ShopHub Admin Dashboard"

All admin pages include:
- Color-coded status badges
- Image previews
- Quick action buttons
- Helpful statistics
- Search and filters

---

**Happy Managing! 🎉**

For technical issues, check the main README.md file.
