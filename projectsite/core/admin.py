# core/admin.py
from django.contrib import admin
from .models import Supplier, Category, Product, PurchaseOrder, PurchaseItem, AuditLog

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
    list_display = ('po_number','date','received','tax_rate','total_subtotal','total_tax','total_amount','cashier')
    search_fields = ('po_number',)
    list_filter = ('date','received','cashier')
    readonly_fields = ('po_number','total_subtotal','total_tax','total_amount')

@admin.register(PurchaseItem)
class PurchaseItemAdmin(admin.ModelAdmin):
    list_display = ('purchase_order','product','quantity','unit_cost')

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('user','action','target','created_at')
    search_fields = ('action','target')
    list_filter = ('user','created_at')
