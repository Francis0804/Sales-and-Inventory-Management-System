# core/models.py
from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal, ROUND_HALF_UP

# ---------- BASE MODEL ----------
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

# ---------- SUPPLIER ----------
class Supplier(BaseModel):
    name = models.CharField(max_length=150)
    contact_person = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    def __str__(self):
        return self.name

# ---------- CATEGORY ----------
class Category(BaseModel):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

# ---------- PRODUCT ----------
class Product(BaseModel):
    code = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    reorder_level = models.IntegerField(default=5)
    quantity = models.IntegerField(default=0)  # materialized for quick read
    def __str__(self):
        return f"{self.code} - {self.name}"

# ---------- PURCHASE ORDER ----------
class PurchaseOrder(BaseModel):
    po_number = models.CharField(max_length=50, unique=True, editable=False)
    date = models.DateField(auto_now_add=True)
    received = models.BooleanField(default=False)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=12, help_text="Tax percentage (e.g., 12 for 12%)")
    total_subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="Subtotal before tax")
    total_tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="Total after tax")
    cash = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    change = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    cashier = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.po_number:
            count = PurchaseOrder.objects.count() + 1
            self.po_number = f"PO-{count:08d}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.po_number

class PurchaseItem(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_cost = models.DecimalField(max_digits=12, decimal_places=2)
    def line_total(self):
        return (self.quantity * self.unit_cost).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

# ---------- AUDIT LOG ----------
class AuditLog(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=150)
    target = models.CharField(max_length=150)
    detail = models.TextField(blank=True)
    def __str__(self):
        return f"{self.user} - {self.action} ({self.target})"
