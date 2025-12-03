# core/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from .models import Category, Product, Supplier, SaleTransaction, PurchaseOrder

class BootstrapFormMixin:
    """Mixin to add Bootstrap styling to form fields"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            widget = field.widget
            css = 'form-control'
            if isinstance(widget, (forms.Select, forms.SelectMultiple)):
                css = 'form-select'
            existing = widget.attrs.get('class', '')
            widget.attrs['class'] = (existing + ' ' + css).strip()
            if not widget.attrs.get('placeholder') and getattr(field, 'label', None):
                widget.attrs.setdefault('placeholder', field.label)

class CategoryForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class ProductForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'code': forms.TextInput(attrs={'placeholder': 'Product code', 'maxlength': 30}),
            'name': forms.TextInput(attrs={'placeholder': 'Product name'}),
            'category': forms.Select(),
            'supplier': forms.Select(),
            'unit_price': forms.NumberInput(attrs={'step': '0.01'}),
            'reorder_level': forms.NumberInput(),
            'quantity': forms.NumberInput(),
        }

class SupplierForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Supplier name'}),
            'contact_person': forms.TextInput(attrs={'placeholder': 'Contact person'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone number'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email address'}),
            'address': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Address'}),
        }

class SaleTransactionForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = SaleTransaction
        fields = '__all__'

class PurchaseOrderForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'
        widgets = {
            'po_number': forms.TextInput(attrs={'placeholder': 'PO number'}),
            'supplier': forms.Select(),
            'received': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class BootstrapPasswordChangeForm(PasswordChangeForm):
    """Custom password change form with Bootstrap styling"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': field.label
            })
