# core/forms.py
from django import forms
from .models import Category, Product, Supplier, SaleTransaction, PurchaseOrder

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'

class SaleTransactionForm(forms.ModelForm):
    class Meta:
        model = SaleTransaction
        fields = '__all__'

class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'
