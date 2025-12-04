# Sales and Inventory Management System

A comprehensive Django-based web application for managing sales, inventory, purchases, and supplier relationships. Built with Django 5.2.7, Bootstrap 5.3.8, and modern Python tools for data management and analysis.

## Overview

This system provides a complete solution for:
- **Product Management**: Manage product catalog with categories, suppliers, and pricing
- **Inventory Tracking**: Real-time inventory monitoring with low-stock alerts
- **Sales Processing**: Record and track sales transactions
- **Purchase Orders**: Manage supplier purchases with tax calculations and status tracking
- **Financial Reports**: Dashboard with key metrics, inventory value, and analytics
- **User Management**: Multi-role user system (Admin/Staff) with authentication

## Project Workflow

### 1. **Authentication & Access Control**
- Login and register pages at `/accounts/login/` and `/accounts/register/`
- Two-tier user roles: Admin (full access) and Staff (limited access)
- Session-based authentication with Django AllAuth

### 2. **Dashboard & Reporting** (`/`)
- Key metrics: Total Products, Total Collected (inventory quantity sum), Inventory Value, Low Stock Items
- Financial summaries and inventory status
- Quick access to all modules

### 3. **Product Management** (`/products/`)
- CRUD operations for products
- Categories for organization
- Supplier associations
- Search and sorting capabilities
- Low stock tracking with reorder level alerts

### 4. **Inventory Management** (`/inventory/`)
- Real-time stock levels per product
- Inventory value calculations (unit price × quantity)
- Low stock status indicators
- Historical tracking

### 5. **Sales Module** (`/sales/`)
- Create and record sales transactions
- Track sales by date, product, and amount
- Search and filter sales records
- Sales history and reporting

### 6. **Purchase Orders** (`/purchases/`)
- Create purchase orders from suppliers
- Status tracking: Received / Pending
- Tax rate calculations (default 12%)
- Financial breakdown: Subtotal, Tax, Total
- Multiple purchase items per order
- Status filter for received vs pending purchases
- Search by PO number, product name, supplier, or date

### 7. **Supplier Management** (`/suppliers/`)
- Maintain supplier information
- Contact details and addresses
- Purchase history association
- Search and management capabilities

### 8. **User Management** (`/users/`)
- Admin user management
- Role assignment (Admin/Staff)
- User detail pages with role badges
- User listing with filtering

## Technical Stack

### Backend
- **Django 5.2.7**: Web framework with ORM
- **Python 3.x**: Core programming language
- **SQLite**: Database (development)
- **Faker**: Test data generation
- **django-allauth**: Authentication system

### Frontend
- **Bootstrap 5.3.8**: Responsive UI framework
- **Bootstrap Icons 1.10.5**: Icon library
- **Custom CSS**: Additional styling
- **JavaScript**: Form validation and interactions

### Tools & Utilities
- **difflib.SequenceMatcher**: String similarity detection for data quality
- **Python Decimal**: Financial calculations precision
- **Django Q objects**: Complex database queries
- **Custom Template Filters**: mul (percentage conversion), add_decimal, currency_format

## Key Features

### 1. **Smart Data Generation**
- Faker-based test data with realistic names and data
- Similarity checking to prevent duplicate product names
- Historical data generation (2022-2025 date range)
- Management command: `python manage.py generate_fake_data`

### 2. **Financial Management**
- Tax rate support (12% default, configurable)
- Precise decimal calculations for money
- Subtotal, tax, and total breakdowns
- Currency formatting across templates

### 3. **Search & Filtering**
- Multi-field search across most modules
- Status filtering for purchases (Received/Pending)
- Sort capabilities (date, amount, ID)
- Pagination (10 items per page)

### 4. **User Interface**
- Responsive Bootstrap 5 design
- Color-coded status indicators (green, yellow, red)
- Consistent form styling
- Mobile-friendly layouts

### 5. **Data Integrity**
- Primary and foreign key relationships
- Cascading deletes where appropriate
- Stock quantity validation
- Tax rate calculations

## Workflow Usage

### Starting the Application
```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Generate test data (optional)
python manage.py generate_fake_data --products 50 --suppliers 15 --purchases 50

# Start development server
python manage.py runserver
```

Visit `http://localhost:8000/` to access the application.

### Common Workflows

#### Adding a New Product
1. Navigate to Products → Add Product
2. Fill in: Code, Name, Category, Supplier, Unit Price, Quantity, Reorder Level
3. Click Save

#### Creating a Purchase Order
1. Navigate to Purchases → Add Purchase
2. Select Supplier and Date
3. Add Items (Product, Quantity, Unit Price)
4. Tax calculated automatically (12%)
5. Mark as Received when items arrive

#### Viewing Dashboard
1. Home page shows all key metrics
2. Total Collected = sum of all product quantities
3. Inventory Value = sum of (unit price × quantity)
4. Low Stock Items = products below reorder level

#### Filtering Purchase Orders
1. Go to Purchases list
2. Use Status dropdown: All Status / Received / Pending
3. Use Search for PO number, product, supplier, or date
4. Use Sort for date or amount ordering

## Directory Structure

```
projectsite/
├── core/                          # Main Django app
│   ├── templates/                 # HTML templates
│   │   ├── accounts/             # Login/Register pages
│   │   ├── products/             # Product templates
│   │   ├── purchases/            # Purchase templates
│   │   ├── sales/                # Sales templates
│   │   ├── suppliers/            # Supplier templates
│   │   ├── users/                # User management
│   │   ├── reports/              # Dashboard
│   │   ├── base.html             # Base template
│   │   └── includes/             # Reusable components
│   ├── management/commands/
│   │   └── generate_fake_data.py # Test data generator
│   ├── migrations/               # Database migrations
│   ├── models.py                 # Database models
│   ├── views.py                  # View controllers
│   ├── forms.py                  # Django forms
│   ├── admin.py                  # Admin configuration
│   └── urls.py                   # URL routing
├── projectsite/                  # Django settings
│   ├── settings.py              # Project configuration
│   ├── urls.py                  # Main URL router
│   └── wsgi.py                  # WSGI application
├── static/                       # Static files (CSS, JS, images)
├── staticfiles/                  # Collected static files
└── db.sqlite3                    # SQLite database
```

## Database Models

### Core Models
- **Product**: Items with price, quantity, category, supplier
- **Category**: Product categories for organization
- **Supplier**: Vendor information and contact
- **User**: Django user with role assignment
- **UserRole**: Admin vs Staff distinction

### Transaction Models
- **PurchaseOrder**: Supplier purchases with date, status, tax
- **PurchaseItem**: Individual items in a purchase
- **Sale**: Sales transactions
- **Inventory**: Product stock tracking

## API & URL Routes

### Public Pages
- `/accounts/login/` - Login page
- `/accounts/register/` - Registration page
- `/` - Dashboard (requires login)

### Admin Areas
- `/admin/` - Django admin panel

### Main Modules (All require login)
- `/products/` - Product listing and management
- `/categories/` - Category management
- `/suppliers/` - Supplier management
- `/purchases/` - Purchase order management
- `/sales/` - Sales tracking
- `/users/` - User management

## Customization

### Adding New Filters
Edit the relevant ListView's `get_queryset()` method in `views.py` to add new filter parameters.

### Modifying Tax Rate
Change the default in `Purchase` model or use the form to set per-purchase.

### Updating Product Categories
Add categories through the Categories admin page.

### Changing Pagination
Update the `paginate_by` value in ListView classes in `views.py`.

## Testing

### Run Faker Data Generation
```bash
# Clear database and generate fresh test data
python manage.py generate_fake_data --clear --products 50 --suppliers 15 --purchases 50

# Generate without clearing (appends data)
python manage.py generate_fake_data --products 30 --suppliers 10 --purchases 20
```

### Manual Testing Checklist
- [ ] Create new product with all fields
- [ ] Add purchase order with multiple items
- [ ] Verify tax calculation (should be 12% of subtotal)
- [ ] Test status filter (Received/Pending)
- [ ] Search purchases by multiple fields
- [ ] Check dashboard metrics update
- [ ] Verify role-based access (Admin vs Staff)

## Troubleshooting

### Database Migration Issues
```bash
python manage.py makemigrations
python manage.py migrate
```

### Static Files Not Loading
```bash
python manage.py collectstatic --noinput
```

### Duplicate Products in Faker Data
Already handled with SequenceMatcher similarity checking (threshold 0.75-0.85).

### Tax Showing as 0%
Use the `mul` template filter: `{{ purchase.tax_rate|mul:100|floatformat:0 }}`

## License

Proprietary - Sales and Inventory Management System

## Support

For issues or feature requests, contact the development team.

---

**Last Updated**: December 4, 2025
**Version**: 1.0
**Status**: Production Ready
