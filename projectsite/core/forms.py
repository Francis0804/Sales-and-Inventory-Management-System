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
        widgets = {
            'code': forms.TextInput(attrs={'placeholder': 'Product code', 'maxlength': 30}),
            'name': forms.TextInput(attrs={'placeholder': 'Product name'}),
            'category': forms.Select(),
            'supplier': forms.Select(),
            'unit_price': forms.NumberInput(attrs={'step': '0.01'}),
            'reorder_level': forms.NumberInput(),
            'quantity': forms.NumberInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to widgets automatically
        for name, field in self.fields.items():
            widget = field.widget
            css = 'form-control'
            # use select styling for choice fields
            if isinstance(widget, (forms.Select, forms.SelectMultiple)):
                css = 'form-select'
            existing = widget.attrs.get('class', '')
            # preserve any existing classes
            widget.attrs['class'] = (existing + ' ' + css).strip()
            # sensible placeholder when not already set
            if not widget.attrs.get('placeholder') and getattr(field, 'label', None):
                widget.attrs.setdefault('placeholder', field.label)

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
