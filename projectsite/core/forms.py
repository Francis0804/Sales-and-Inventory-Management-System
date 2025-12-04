# core/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from .models import Category, Product, Supplier, PurchaseOrder, PurchaseItem

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
        # exclude reorder_level from product forms
        exclude = ['reorder_level']
        widgets = {
            'code': forms.TextInput(attrs={'placeholder': 'Product code', 'maxlength': 30}),
            'name': forms.TextInput(attrs={'placeholder': 'Product name'}),
            'category': forms.Select(),
            'supplier': forms.Select(),
            'unit_price': forms.NumberInput(attrs={'step': '0.01'}),
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

class PurchaseOrderForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ['tax_rate', 'cash', 'total_tax', 'total_subtotal', 'cashier']
        widgets = {
            'tax_rate': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'Tax %'}),
            'cash': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'Cash received'}),
            'total_tax': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'Total tax', 'readonly': True}),
            'total_subtotal': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'Subtotal', 'readonly': True}),
            'cashier': forms.Select(),
        }

class PurchaseItemForm(forms.ModelForm):
    """Form for adding items to purchase order"""
    class Meta:
        model = PurchaseItem
        fields = ['product', 'quantity', 'unit_cost']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantity', 'min': '1'}),
            'unit_cost': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Unit cost', 'step': '0.01'}),
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

class UserProfileForm(BootstrapFormMixin, forms.ModelForm):
    """Form for editing user profile information"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email address'}),
        }
