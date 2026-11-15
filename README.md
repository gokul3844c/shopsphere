# ShopSphere — Amazon-Inspired E-Commerce Platform

ShopSphere is a full-featured, functional Amazon-inspired e-commerce web application built using Python Django, SQLite, HTML5, Vanilla CSS3, and JavaScript.

---

## 🌟 Key Features

1. **Authentication & User Management**:
   - Immediate login redirect for unauthenticated users accessing protected routes.
   - Dual login credentials: sign in via either username or email address.
   - Password show/hide toggle.
   - "Remember Me" session management (14 days vs. browser session).
   - Forgot password & password reset workflow with email link generation.
   - Registration flow with auto-provisioned `UserProfile`.
   - Customer account dashboard with saved address book management (Add, Edit, Delete, Set Default).

2. **Amazon-Inspired Modern UI/UX**:
   - Dark Navy navigation bar (`#131921`) with location widget, department selector, search bar, language/currency badge (`🇮🇳 EN`), Account & Lists dropdown, Orders, and Cart counter.
   - Subnav with department quick-links and Today's Deals.
   - Promotional hero banner and Amazon-style 4-card quad grids.
   - Product cards with star ratings, verified review counts, Prime badges, and Deal tags.
   - Indian Rupee (`₹`) pricing with original MRP strikethroughs and savings calculations.
   - Multi-column product details page with image switcher gallery, technical specifications table, Buy Box with In-Stock / Low Stock indicators, and customer review submission.

3. **Catalogue & Search System**:
   - 104 realistic demo products across 8 categories:
     - Electronics
     - Computers
     - Mobile Phones
     - Fashion
     - Home and Kitchen
     - Books
     - Sports
     - Beauty
   - Fast full-text search across product name, brand, description, and department.
   - Live debounced search suggestions dropdown in the header.
   - Multi-criteria filters: Department, Customer Reviews (4★+, 3★+), Price Range (₹ Min/Max), and In-Stock status.
   - Sorting: Featured, Price: Low to High, Price: High to Low, Customer Rating, and Newest Arrivals.
   - Clean pagination (16 items per page).

4. **Cart & Inventory Management**:
   - Real-time cart synchronization between sessions and database models (`Cart` and `CartItem`).
   - AJAX quantity steppers (+/-) and deletion with instantaneous subtotal and header badge updates.
   - Server-side inventory validation preventing additions beyond available stock.
   - Free delivery threshold calculation (Orders over ₹499 qualify for Free Delivery, else ₹49).

5. **Atomic Checkout & Orders**:
   - Step 1: Select saved delivery address or enter a new address.
   - Step 2: Payment method options:
     - Cash on Delivery (COD)
     - Simulated Credit/Debit Card
     - Simulated UPI / QR
     - Simulated Net Banking
   - Step 3: Review items and delivery options.
   - Database row-level locking via `select_for_update()` inside atomic transactions ensuring zero race conditions in inventory.
   - Order confirmation with tracking timeline (`OD-XXXXXXXX`).
   - Order history with status badges (`Order Placed`, `Confirmed`, `Shipped`, `Delivered`, `Cancelled`).
   - Customer order cancellation before shipping with automated inventory restoration.
   - Strictly enforced access permissions ensuring customers only view their own orders.

---

## 🛠️ Technology Stack

- **Backend**: Python 3.11+, Django 5.x
- **Database**: SQLite3
- **Frontend**: HTML5, Vanilla CSS3 (Custom Amazon design tokens), Vanilla JavaScript
- **Image Processing**: Pillow (local SVGs and media images in `media/products/`)

---

## 🚀 Installation & Setup Instructions

### 1. Create and Activate Virtual Environment
```bash
# Windows
python -m venv .venv
.\.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Apply Database Migrations
```bash
python manage.py makemigrations accounts catalog cart orders
python manage.py migrate
```

### 4. Seed the Catalogue (104 Demo Products across 8 Categories)
```bash
python manage.py seed_products
```
*Note: This command is completely idempotent and safe to run multiple times without creating duplicates.*

### 5. Create an Administrator Account
```bash
python manage.py createsuperuser
```

### 6. Run the Development Server
```bash
python manage.py runserver
```
Visit **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)** in your browser.

---

## 🧪 Running Automated Tests

Run the full automated test suite covering authentication, catalog search/filters, cart calculations, inventory concurrency, order access control, and full end-to-end user journeys:

```bash
python manage.py test accounts catalog cart orders tests
```

---

## 📂 Project Structure

```text
shopsphere/
├── manage.py
├── requirements.txt
├── .env.example
├── README.md
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── accounts/
│   ├── models.py          # UserProfile with auto-create signals
│   ├── views.py           # Login, registration, address book, password reset
│   ├── forms.py           # Email/username login, registration, profile forms
│   ├── urls.py            # Account routes
│   └── tests.py           # Authentication & permission tests
├── catalog/
│   ├── models.py          # Category, Product, ProductImage, Review
│   ├── views.py           # Homepage, product listing, details, live search
│   ├── admin.py           # Admin interface with inlines and filters
│   ├── urls.py            # Catalog routes
│   ├── fixtures/
│   │   ├── products.json  # 104 demo products dataset
│   │   └── image_manifest.json
│   └── management/commands/
│       └── seed_products.py # Idempotent seed command
├── cart/
│   ├── models.py          # Cart and CartItem models
│   ├── views.py           # Add, update, remove, clear, subtotal calculations
│   ├── context_processors.py # Header live cart badge count
│   ├── urls.py            # Cart routes
│   └── tests.py           # Cart operations & stock limit tests
├── orders/
│   ├── models.py          # Address, Order, OrderItem, Payment
│   ├── views.py           # Atomic checkout, confirmation, history, cancel
│   ├── forms.py           # AddressForm with PIN & phone validation
│   ├── admin.py           # OrderAdmin with status update actions
│   ├── urls.py            # Order routes
│   └── tests.py           # Checkout, inventory lock & owner isolation tests
├── templates/
│   ├── base.html          # Dark navy topbar, search, subnav, footer
│   ├── accounts/          # Login, register, profile, address, password reset
│   ├── catalog/           # Home, product_list, product_detail
│   ├── cart/              # Cart table, sticky summary, empty states
│   └── orders/            # Checkout, confirmation, history, detail
├── static/
│   ├── css/style.css      # Amazon-inspired design system
│   ├── css/responsive.css # Responsive breakpoints
│   ├── js/main.js         # Password toggler, notifications, thumbnail gallery
│   ├── js/search.js       # Live search suggestions
│   └── js/cart.js         # Dynamic AJAX cart updates
├── media/products/        # Generated local SVG & image product assets
└── tests/
    └── test_user_flow.py  # End-to-end customer purchase journey test
```
