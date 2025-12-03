# core/views.py

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Sum, F, Q
from .models import Category, Product, Supplier, SaleTransaction, PurchaseOrder
from .forms import CategoryForm, ProductForm, SupplierForm, SaleTransactionForm, PurchaseOrderForm, BootstrapPasswordChangeForm, UserProfileForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.shortcuts import redirect

# ---------- HOME PAGE ----------
def home(request):
    from decimal import Decimal
    
    # Basic counts
    total_products = Product.objects.count()
    total_suppliers = Supplier.objects.count()
    total_sales = SaleTransaction.objects.count()
    total_purchases = PurchaseOrder.objects.count()
    
    # Stock info
    low_stock_products = Product.objects.filter(quantity__lt=F('reorder_level')).count()
    out_of_stock = Product.objects.filter(quantity=0).count()
    
    # Sales info
    total_sales_amount = SaleTransaction.objects.aggregate(Sum('total'))['total__sum'] or Decimal('0.00')
    
    # Purchase info
    pending_purchases = PurchaseOrder.objects.filter(received=False).count()
    total_purchase_amount = PurchaseOrder.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or Decimal('0.00')
    
    context = {
        'total_products': total_products,
        'total_suppliers': total_suppliers,
        'total_sales': total_sales,
        'total_purchases': total_purchases,
        'low_stock_products': low_stock_products,
        'out_of_stock': out_of_stock,
        'total_sales_amount': total_sales_amount,
        'pending_purchases': pending_purchases,
        'total_purchase_amount': total_purchase_amount,
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

    def get_queryset(self):
        qs = super().get_queryset()

        q = self.request.GET.get("q")
        sort = self.request.GET.get("sort")

        # SEARCH
        if q:
            qs = qs.filter(name__icontains=q)

        # SORT
        allowed_sorts = ['name', '-name', 'id', '-id', 'created_at', '-created_at']
        if sort in allowed_sorts:
            qs = qs.order_by(sort)
        else:
            qs = qs.order_by("name")   # default

        return qs



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




# ========================================
#                PRODUCT
# ========================================
class ProductListView(ListView):
    model = Product
    template_name = 'products_list.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()

        q = self.request.GET.get("q")
        sort = self.request.GET.get("sort")

        # SEARCH
        if q:
            qs = qs.filter(
                Q(name__icontains=q) |
                Q(description__icontains=q) |
                Q(category__name__icontains=q)
            ).distinct()

        # SORT
        allowed_sorts = [
            'name', '-name',
            'price', '-price',
            'stock', '-stock',
            'created_at', '-created_at',
            'id', '-id'
        ]

        if sort in allowed_sorts:
            qs = qs.order_by(sort)
        else:
            qs = qs.order_by("-id")  # default newest first

        return qs



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




# ========================================
#                SUPPLIER
# ========================================
class SupplierListView(ListView):
    model = Supplier
    template_name = 'suppliers_list.html'
    context_object_name = 'suppliers'

    def get_queryset(self):
        qs = super().get_queryset()

        q = self.request.GET.get("q")
        sort = self.request.GET.get("sort")

        # SEARCH
        if q:
            qs = qs.filter(
                Q(name__icontains=q) |
                Q(address__icontains=q) |
                Q(contact_person__icontains=q) |
                Q(phone__icontains=q) |
                Q(email__icontains=q)
            ).distinct()

        # SORT
        allowed_sorts = [
            'name', '-name',
            'contact_person', '-contact_person',
            'created_at', '-created_at',
            'id', '-id'
        ]

        if sort in allowed_sorts:
            qs = qs.order_by(sort)
        else:
            qs = qs.order_by("name")  # default

        return qs



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




# ========================================
#                 SALES
# ========================================
class SalesListView(ListView):
    model = SaleTransaction
    template_name = 'sales_list.html'
    context_object_name = 'sales'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()

        q = self.request.GET.get("q")
        sort = self.request.GET.get("sort")

        # SEARCH
        if q:
            qs = qs.filter(
                Q(items__product__name__icontains=q) |
                Q(sale_number__icontains=q) |
                Q(date__icontains=q)
            ).distinct()

        # SORT
        allowed_sorts = [
            'date', '-date',
            'total_amount', '-total_amount',
            'id', '-id'
        ]

        if sort in allowed_sorts:
            qs = qs.order_by(sort)
        else:
            qs = qs.order_by("-date")  # newest first

        return qs



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




# ========================================
#                PURCHASES
# ========================================
class PurchaseListView(ListView):
    model = PurchaseOrder
    template_name = 'purchases_list.html'
    context_object_name = 'purchases'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()

        q = self.request.GET.get("q")
        sort = self.request.GET.get("sort")

        # SEARCH
        if q:
            qs = qs.filter(
                Q(items__product__name__icontains=q) |
                Q(supplier__name__icontains=q) |
                Q(po_number__icontains=q) |
                Q(date__icontains=q)
            ).distinct()

        # SORT
        allowed_sorts = [
            'date', '-date',
            'total_amount', '-total_amount',
            'id', '-id'
        ]

        if sort in allowed_sorts:
            qs = qs.order_by(sort)
        else:
            qs = qs.order_by("-date")  # default

        return qs



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


# ---------- PROFILE ----------
def profile(request):
    """Display and handle user profile information and password changes"""
    if request.method == 'POST':
        # Handle password change form submission
        password_form = BootstrapPasswordChangeForm(request.user, request.POST)
        if password_form.is_valid():
            password_form.save()
            # Show success message
            from django.contrib import messages
            messages.success(request, 'Your password has been changed successfully!')
            return redirect('profile')
    else:
        password_form = BootstrapPasswordChangeForm(request.user)
    
    context = {
        'user': request.user,
        'password_form': password_form,
    }
    return render(request, 'profile.html', context)


def edit_profile(request):
    """Edit user profile information"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            from django.contrib import messages
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    context = {
        'form': form,
    }
    return render(request, 'edit_profile.html', context)