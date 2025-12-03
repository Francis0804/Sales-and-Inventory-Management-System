# core/views.py
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Category, Product, Supplier, SaleTransaction, PurchaseOrder
from .forms import CategoryForm, ProductForm, SupplierForm, SaleTransactionForm, PurchaseOrderForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.shortcuts import redirect

# ---------- HOME PAGE ----------
def home(request):
    """Dashboard summary for Sales and Inventory Management System"""
    total_products = Product.objects.count()
    total_suppliers = Supplier.objects.count()
    total_sales = SaleTransaction.objects.count()
    total_purchases = PurchaseOrder.objects.count()

    context = {
        'total_products': total_products,
        'total_suppliers': total_suppliers,
        'total_sales': total_sales,
        'total_purchases': total_purchases,
    }
    return render(request, 'home.html', context)


def register(request):
    """Simple registration view using Django's UserCreationForm."""
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                auth_login(request, user)
                return redirect('login')
        else:
            form = UserCreationForm()
        return render(request, 'accounts/register.html', {'form': form})
    else:
        return redirect('home')


# ---------- CATEGORY ----------
class CategoryListView(ListView):
    model = Category
    template_name = 'categories_list.html'
    context_object_name = 'categories'
    paginate_by = 10


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'categories_form.html'
    success_url = reverse_lazy('categories-list')


class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'categories_form.html'
    success_url = reverse_lazy('categories-list')


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'categories_confirm_delete.html'
    success_url = reverse_lazy('categories-list')


# ---------- PRODUCT ----------
class ProductListView(ListView):
    model = Product
    template_name = 'products_list.html'
    context_object_name = 'products'
    paginate_by = 10


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products_form.html'
    success_url = reverse_lazy('products-list')


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products_form.html'
    success_url = reverse_lazy('products-list')


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'products_confirm_delete.html'
    success_url = reverse_lazy('products-list')


# ---------- SUPPLIER ----------
class SupplierListView(ListView):
    model = Supplier
    template_name = 'suppliers_list.html'
    context_object_name = 'suppliers'
    paginate_by = 10


class SupplierCreateView(CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'suppliers_form.html'
    success_url = reverse_lazy('suppliers-list')


class SupplierUpdateView(UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'suppliers_form.html'
    success_url = reverse_lazy('suppliers-list')


class SupplierDeleteView(DeleteView):
    model = Supplier
    template_name = 'suppliers_confirm_delete.html'
    success_url = reverse_lazy('suppliers-list')


# ---------- SALES ----------
class SalesListView(ListView):
    model = SaleTransaction
    template_name = 'sales_list.html'
    context_object_name = 'sales'
    paginate_by = 10


class SalesCreateView(CreateView):
    model = SaleTransaction
    form_class = SaleTransactionForm
    template_name = 'sales_form.html'
    success_url = reverse_lazy('sales-list')


class SalesUpdateView(UpdateView):
    model = SaleTransaction
    form_class = SaleTransactionForm
    template_name = 'sales_form.html'
    success_url = reverse_lazy('sales-list')


class SalesDeleteView(DeleteView):
    model = SaleTransaction
    template_name = 'sales_confirm_delete.html'
    success_url = reverse_lazy('sales-list')


# ---------- PURCHASES ----------
class PurchaseListView(ListView):
    model = PurchaseOrder
    template_name = 'purchases_list.html'
    context_object_name = 'purchases'
    paginate_by = 10


class PurchaseCreateView(CreateView):
    model = PurchaseOrder
    form_class = PurchaseOrderForm
    template_name = 'purchases_form.html'
    success_url = reverse_lazy('purchases-list')


class PurchaseUpdateView(UpdateView):
    model = PurchaseOrder
    form_class = PurchaseOrderForm
    template_name = 'purchases_form.html'
    success_url = reverse_lazy('purchases-list')


class PurchaseDeleteView(DeleteView):
    model = PurchaseOrder
    template_name = 'purchases_confirm_delete.html'
    success_url = reverse_lazy('purchases-list')
