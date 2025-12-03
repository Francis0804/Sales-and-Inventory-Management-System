# core/views.py

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.db.models import Sum, F, Q
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Category, Product, Supplier, PurchaseOrder, PurchaseItem
from .forms import CategoryForm, ProductForm, SupplierForm, PurchaseOrderForm, PurchaseItemForm, BootstrapPasswordChangeForm, UserProfileForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.http import JsonResponse
from decimal import Decimal
import json

# Helper function to convert products to JSON-serializable format
def serialize_products(products_qs):
    """Convert product queryset to JSON-serializable list"""
    products_list = []
    for p in products_qs:
        products_list.append({
            'id': p.id,
            'code': p.code,
            'name': p.name,
            'unit_price': float(p.unit_price),
            'quantity': p.quantity
        })
    return products_list

# ---------- HOME PAGE ----------
def home(request):
    from decimal import Decimal
    from datetime import datetime, timedelta
    from django.utils import timezone
    
    # Basic counts
    total_products = Product.objects.count()
    total_suppliers = Supplier.objects.count()
    total_purchases = PurchaseOrder.objects.count()
    
    # Stock info
    low_stock_products = Product.objects.filter(quantity__lt=F('reorder_level')).count()
    out_of_stock = Product.objects.filter(quantity=0).count()
    
    # Purchase info
    pending_purchases = PurchaseOrder.objects.filter(received=False).count()
    total_purchase_amount = PurchaseOrder.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or Decimal('0.00')
    total_tax_amount = PurchaseOrder.objects.aggregate(Sum('total_tax'))['total_tax__sum'] or Decimal('0.00')
    
    # Time-based metrics
    now = timezone.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)
    
    # This week (Monday to current day)
    week_start = now - timedelta(days=now.weekday())
    week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
    
    # This month
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # This year
    year_start = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # Today's purchases
    today_purchases = PurchaseOrder.objects.filter(created_at__gte=today_start, created_at__lt=today_end).count()
    today_purchase_amount = PurchaseOrder.objects.filter(created_at__gte=today_start, created_at__lt=today_end).aggregate(Sum('total_amount'))['total_amount__sum'] or Decimal('0.00')
    today_tax_amount = PurchaseOrder.objects.filter(created_at__gte=today_start, created_at__lt=today_end).aggregate(Sum('total_tax'))['total_tax__sum'] or Decimal('0.00')
    
    # This week's purchases
    week_purchases = PurchaseOrder.objects.filter(created_at__gte=week_start, created_at__lt=now).count()
    week_purchase_amount = PurchaseOrder.objects.filter(created_at__gte=week_start, created_at__lt=now).aggregate(Sum('total_amount'))['total_amount__sum'] or Decimal('0.00')
    week_tax_amount = PurchaseOrder.objects.filter(created_at__gte=week_start, created_at__lt=now).aggregate(Sum('total_tax'))['total_tax__sum'] or Decimal('0.00')
    
    # This month's purchases
    month_purchases = PurchaseOrder.objects.filter(created_at__gte=month_start, created_at__lt=now).count()
    month_purchase_amount = PurchaseOrder.objects.filter(created_at__gte=month_start, created_at__lt=now).aggregate(Sum('total_amount'))['total_amount__sum'] or Decimal('0.00')
    month_tax_amount = PurchaseOrder.objects.filter(created_at__gte=month_start, created_at__lt=now).aggregate(Sum('total_tax'))['total_tax__sum'] or Decimal('0.00')
    
    # This year's purchases
    year_purchases = PurchaseOrder.objects.filter(created_at__gte=year_start, created_at__lt=now).count()
    year_purchase_amount = PurchaseOrder.objects.filter(created_at__gte=year_start, created_at__lt=now).aggregate(Sum('total_amount'))['total_amount__sum'] or Decimal('0.00')
    year_tax_amount = PurchaseOrder.objects.filter(created_at__gte=year_start, created_at__lt=now).aggregate(Sum('total_tax'))['total_tax__sum'] or Decimal('0.00')
    
    context = {
        'total_products': total_products,
        'total_suppliers': total_suppliers,
        'total_purchases': total_purchases,
        'low_stock_products': low_stock_products,
        'out_of_stock': out_of_stock,
        'pending_purchases': pending_purchases,
        'total_purchase_amount': total_purchase_amount,
        'total_tax_amount': total_tax_amount,
        # Today
        'today_purchases': today_purchases,
        'today_purchase_amount': today_purchase_amount,
        'today_tax_amount': today_tax_amount,
        # This week
        'week_purchases': week_purchases,
        'week_purchase_amount': week_purchase_amount,
        'week_tax_amount': week_tax_amount,
        # This month
        'month_purchases': month_purchases,
        'month_purchase_amount': month_purchase_amount,
        'month_tax_amount': month_tax_amount,
        # This year
        'year_purchases': year_purchases,
        'year_purchase_amount': year_purchase_amount,
        'year_tax_amount': year_tax_amount,
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
        category = self.request.GET.get("category")
        supplier = self.request.GET.get("supplier")

        # SEARCH
        if q:
            qs = qs.filter(
                Q(name__icontains=q) |
                Q(description__icontains=q) |
                Q(category__name__icontains=q)
            ).distinct()

        # FILTER BY CATEGORY
        if category:
            qs = qs.filter(category_id=category)

        # FILTER BY SUPPLIER
        if supplier:
            qs = qs.filter(supplier_id=supplier)

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['suppliers'] = Supplier.objects.all()
        context['selected_category'] = self.request.GET.get("category", "")
        context['selected_supplier'] = self.request.GET.get("supplier", "")
        context['search_query'] = self.request.GET.get("q", "")
        return context



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


class PurchaseDetailView(LoginRequiredMixin, DetailView):
    model = PurchaseOrder
    template_name = 'purchases_detail.html'
    context_object_name = 'purchase'
    login_url = 'login'

    def post(self, request, *args, **kwargs):
        purchase = self.get_object()
        action = request.POST.get('action')
        
        if action == 'mark_received':
            purchase.received = True
            purchase.save()
            from django.contrib import messages
            messages.success(request, 'Purchase marked as received!')
        
        return redirect('purchases-detail', pk=purchase.id)

class PurchaseCreateView(CreateView):
    model = PurchaseOrder
    form_class = PurchaseOrderForm
    template_name = 'purchases_form.html'
    success_url = reverse_lazy('purchases-list')

    def get_context_data(self, **kwargs):
        # Don't call super() to avoid accessing self.object which doesn't exist in CreateView
        context = kwargs
        if 'form' not in context:
            context['form'] = self.get_form()
        products_qs = Product.objects.all()
        context['products'] = products_qs
        context['products_json'] = json.dumps(serialize_products(products_qs))
        context['item_form'] = PurchaseItemForm()
        return context

    def post(self, request, *args, **kwargs):
        # Check if this is an AJAX request for product details
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            product_id = request.POST.get('product_id')
            try:
                product = Product.objects.get(id=product_id)
                return JsonResponse({
                    'success': True,
                    'product_name': product.name,
                    'unit_price': str(product.unit_price),
                    'available_quantity': product.quantity,
                })
            except Product.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Product not found'})
        
        # Regular form submission
        form = self.get_form()
        if form.is_valid():
            purchase_order = form.save(commit=False)
            purchase_order.cashier = request.user
            purchase_order.save()  # Save first to get the PO number and primary key
            
            # Add purchase items from form
            items_data = request.POST.getlist('product_id')
            quantities = request.POST.getlist('quantity')
            unit_costs = request.POST.getlist('unit_cost')
            
            total_subtotal = Decimal('0.00')
            total_tax = Decimal('0.00')
            
            for product_id, quantity, unit_cost in zip(items_data, quantities, unit_costs):
                if product_id and quantity and unit_cost:
                    try:
                        product = Product.objects.get(id=product_id)
                        qty = int(quantity)
                        cost = Decimal(unit_cost)
                        line_total = qty * cost
                        
                        PurchaseItem.objects.create(
                            purchase_order=purchase_order,
                            product=product,
                            quantity=qty,
                            unit_cost=cost
                        )
                        
                        # Decrement product stock
                        product.quantity -= qty
                        product.save()
                        
                        total_subtotal += line_total
                        # Calculate tax on this line item based on purchase order tax rate
                        line_tax = (line_total * purchase_order.tax_rate / Decimal('100')).quantize(Decimal('0.01'))
                        total_tax += line_tax
                    except (Product.DoesNotExist, ValueError):
                        continue
            
            purchase_order.total_subtotal = total_subtotal
            purchase_order.total_tax = total_tax
            purchase_order.total_amount = total_subtotal + total_tax
            
            # Calculate change if cash is provided
            if purchase_order.cash:
                cash = Decimal(str(purchase_order.cash))
                purchase_order.change = (cash - purchase_order.total_amount).quantize(Decimal('0.01'))
            
            purchase_order.save()
            
            from django.contrib import messages
            messages.success(request, 'Purchase order created successfully!')
            return redirect('purchases-list')
            # Return to form with errors - build context manually
            products_qs = Product.objects.all()
            context = {
                'form': form,
                'products': products_qs,
                'products_json': json.dumps(serialize_products(products_qs)),
                'item_form': PurchaseItemForm(),
            }
            return self.render_to_response(context)


class PurchaseUpdateView(UpdateView):
    model = PurchaseOrder
    form_class = PurchaseOrderForm
    template_name = 'purchases_form.html'
    success_url = reverse_lazy('purchases-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products_qs = Product.objects.all()
        context['products'] = products_qs
        context['products_json'] = json.dumps(serialize_products(products_qs))
        context['item_form'] = PurchaseItemForm()
        # Add existing items to context for display
        context['existing_items'] = self.object.items.all() if self.object else []
        context['is_received'] = self.object.received if self.object else False
        return context

    def post(self, request, *args, **kwargs):
        purchase_order = self.get_object()
        
        # Prevent editing if purchase order has been received
        if purchase_order.received:
            from django.contrib import messages
            messages.error(request, 'Cannot edit a received purchase order.')
            return redirect('purchases-list')
        
        form = self.get_form()
        if form.is_valid():
            purchase_order = self.get_object()
            
            # Restore stock from old items before deleting
            old_items = purchase_order.items.all()
            for old_item in old_items:
                old_item.product.quantity += old_item.quantity
                old_item.product.save()
            
            # Clear existing items
            purchase_order.items.all().delete()
            
            # Update cashier to current user
            purchase_order.cashier = request.user
            
            # Add new items from form
            items_data = request.POST.getlist('product_id')
            quantities = request.POST.getlist('quantity')
            unit_costs = request.POST.getlist('unit_cost')
            
            total_subtotal = Decimal('0.00')
            total_tax = Decimal('0.00')
            
            for product_id, quantity, unit_cost in zip(items_data, quantities, unit_costs):
                if product_id and quantity and unit_cost:
                    try:
                        product = Product.objects.get(id=product_id)
                        qty = int(quantity)
                        cost = Decimal(unit_cost)
                        line_total = qty * cost
                        
                        PurchaseItem.objects.create(
                            purchase_order=purchase_order,
                            product=product,
                            quantity=qty,
                            unit_cost=cost
                        )
                        
                        # Decrement product stock
                        product.quantity -= qty
                        product.save()
                        
                        total_subtotal += line_total
                        # Calculate tax on this line item based on purchase order tax rate
                        line_tax = (line_total * purchase_order.tax_rate / Decimal('100')).quantize(Decimal('0.01'))
                        total_tax += line_tax
                    except (Product.DoesNotExist, ValueError):
                        continue
            
            purchase_order.total_subtotal = total_subtotal
            purchase_order.total_tax = total_tax
            purchase_order.total_amount = total_subtotal + total_tax
            
            # Calculate change if cash is provided
            if purchase_order.cash:
                cash = Decimal(str(purchase_order.cash))
                purchase_order.change = (cash - purchase_order.total_amount).quantize(Decimal('0.01'))
            
            purchase_order.save()
            
            from django.contrib import messages
            messages.success(request, 'Purchase order updated successfully!')
            return redirect('purchases-list')
        else:
            context = self.get_context_data()
            context['form'] = form
            return self.render_to_response(context)


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