# core/management/commands/create_initial_data.py
from django.core.management.base import BaseCommand
from decimal import Decimal
from django.contrib.auth.models import User
from core.models import Category, Supplier, Product, PurchaseOrder, PurchaseItem, SaleTransaction, SaleItem

class Command(BaseCommand):
    help = "Create initial sample records (categories, suppliers, products, orders, sales, users)"

    def handle(self, *args, **options):
        # Users
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')
            self.stdout.write("Created superuser 'admin' (password: adminpass)")

        if not User.objects.filter(username='cashier').exists():
            User.objects.create_user('cashier', 'cashier@example.com', 'cashierpass', is_staff=True)
            self.stdout.write("Created user 'cashier' (password: cashierpass)")

        if not User.objects.filter(username='inventory').exists():
            User.objects.create_user('inventory', 'inventory@example.com', 'inventorypass', is_staff=True)
            self.stdout.write("Created user 'inventory' (password: inventorypass)")

        # Categories (8)
        categories = ["Beverages","Snacks","Stationery","Electronics","Cleaning Supplies","Office Equipment","Personal Care","Others"]
        created_cats = []
        for name in categories:
            cat, _ = Category.objects.get_or_create(name=name)
            created_cats.append(cat)
        self.stdout.write("Created/checked 8 categories")

        # Suppliers (2)
        s1, _ = Supplier.objects.get_or_create(name="ABC Distributors", defaults={
            'contact_person':'Maria Santos','phone':'09171234567','email':'abc@example.com','address':'Manila'
        })
        s2, _ = Supplier.objects.get_or_create(name="MegaMart Trading", defaults={
            'contact_person':'John Dela Cruz','phone':'09281112222','email':'megamart@example.com','address':'Quezon City'
        })
        self.stdout.write("Created/checked 2 suppliers")

        # Products (10)
        products = [
            ("PRD-001","Ballpen", "Stationery", s1, '15.00', 50, 200),
            ("PRD-002","Notebook","Stationery", s1, '45.00', 30, 150),
            ("PRD-003","Coffee","Beverages", s2, '120.00', 20, 60),
            ("PRD-004","Chips","Snacks", s2, '35.00', 25, 80),
            ("PRD-005","Liquid Soap","Cleaning Supplies", s1, '75.00', 10, 40),
            ("PRD-006","Printer Paper (A4)","Office Equipment", s1, '250.00', 15, 100),
            ("PRD-007","Laptop","Electronics", s2, '35000.00', 3, 10),
            ("PRD-008","Mouse","Electronics", s2, '500.00', 10, 25),
            ("PRD-009","Shampoo","Personal Care", s1, '120.00', 20, 50),
            ("PRD-010","Toothpaste","Personal Care", s1, '90.00', 20, 45),
        ]
        for code,name,cat_name,supplier,price,reorder,qty in products:
            cat = Category.objects.get(name=cat_name)
            prod, created = Product.objects.get_or_create(code=code, defaults={
                'name':name, 'category':cat, 'supplier':supplier, 'unit_price':Decimal(price),
                'reorder_level':reorder, 'quantity':qty
            })
        self.stdout.write("Created/checked 10 products")

        # Purchase Orders (2)
        po1, _ = PurchaseOrder.objects.get_or_create(po_number="PO-0001", defaults={'supplier':s1,'received':True,'total_amount':Decimal('4500.00')})
        po2, _ = PurchaseOrder.objects.get_or_create(po_number="PO-0002", defaults={'supplier':s2,'received':True,'total_amount':Decimal('36000.00')})
        # Purchase items for PO1
        PurchaseItem.objects.get_or_create(purchase_order=po1, product=Product.objects.get(code="PRD-001"), defaults={'quantity':100,'unit_cost':Decimal('12.00')})
        PurchaseItem.objects.get_or_create(purchase_order=po1, product=Product.objects.get(code="PRD-002"), defaults={'quantity':50,'unit_cost':Decimal('40.00')})
        # Purchase items for PO2
        PurchaseItem.objects.get_or_create(purchase_order=po2, product=Product.objects.get(code="PRD-007"), defaults={'quantity':5,'unit_cost':Decimal('33000.00')})
        PurchaseItem.objects.get_or_create(purchase_order=po2, product=Product.objects.get(code="PRD-008"), defaults={'quantity':10,'unit_cost':Decimal('450.00')})
        self.stdout.write("Created/checked 2 purchase orders with items")

        # Sale Transactions (2) with tax auto-calculation
        admin = User.objects.get(username='admin')
        sale1, created = SaleTransaction.objects.get_or_create(sale_number="SALE-0001", defaults={'cashier':admin,'subtotal':Decimal('535.71'),'cash':Decimal('1000.00')})
        sale2, created = SaleTransaction.objects.get_or_create(sale_number="SALE-0002", defaults={'cashier':admin,'subtotal':Decimal('267.86'),'cash':Decimal('500.00')})
        # add Sale Items
        SaleItem.objects.get_or_create(sale=sale1, product=Product.objects.get(code="PRD-001"), defaults={'quantity':10,'price':Decimal('15.00')})
        SaleItem.objects.get_or_create(sale=sale2, product=Product.objects.get(code="PRD-003"), defaults={'quantity':2,'price':Decimal('120.00')})
        SaleItem.objects.get_or_create(sale=sale2, product=Product.objects.get(code="PRD-004"), defaults={'quantity':1,'price':Decimal('60.00')})
        self.stdout.write("Created/checked 2 sale transactions with items")

        self.stdout.write(self.style.SUCCESS("Initial data creation completed."))
