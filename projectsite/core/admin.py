# core/admin.py
from django.contrib import admin
from .models import Supplier, Category, Product, PurchaseOrder, PurchaseItem, SaleTransaction, SaleItem, AuditLog

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('created_at',)

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'phone', 'email', 'created_at')
    search_fields = ('name','contact_person')
    list_filter = ('created_at',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('code','name','category','supplier','quantity','unit_price','reorder_level')
    search_fields = ('name','code')
    list_filter = ('category','supplier')

@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('po_number','supplier','date','received','total_amount')
    search_fields = ('po_number','supplier__name')
    list_filter = ('supplier','date')

@admin.register(PurchaseItem)
class PurchaseItemAdmin(admin.ModelAdmin):
    list_display = ('purchase_order','product','quantity','unit_cost')

@admin.register(SaleTransaction)
class SaleTransactionAdmin(admin.ModelAdmin):
    list_display = ('sale_number','cashier','date','subtotal','tax','total','cash','change')
    search_fields = ('sale_number','cashier__username')
    list_filter = ('cashier','date')

@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ('sale','product','quantity','price')

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('user','action','target','created_at')
    search_fields = ('action','target')
    list_filter = ('user','created_at')
