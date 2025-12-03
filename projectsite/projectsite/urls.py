from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Home
    path('', views.home, name='home'),
    
    # Login & Logout
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),

    # Categories
    path('categories/', views.CategoryListView.as_view(), name='categories-list'),
    path('categories/add/', views.CategoryCreateView.as_view(), name='categories-add'),
    path('categories/<int:pk>/edit/', views.CategoryUpdateView.as_view(), name='categories-edit'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='categories-delete'),

    # Products
    path('products/', views.ProductListView.as_view(), name='products-list'),
    path('products/add/', views.ProductCreateView.as_view(), name='products-add'),
    path('products/<int:pk>/edit/', views.ProductUpdateView.as_view(), name='products-edit'),
    path('products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='products-delete'),

    # Suppliers
    path('suppliers/', views.SupplierListView.as_view(), name='suppliers-list'),
    path('suppliers/add/', views.SupplierCreateView.as_view(), name='suppliers-add'),
    path('suppliers/<int:pk>/edit/', views.SupplierUpdateView.as_view(), name='suppliers-edit'),
    path('suppliers/<int:pk>/delete/', views.SupplierDeleteView.as_view(), name='suppliers-delete'),

    # Sales
    path('sales/', views.SalesListView.as_view(), name='sales-list'),
    path('sales/add/', views.SalesCreateView.as_view(), name='sales-add'),
    path('sales/<int:pk>/edit/', views.SalesUpdateView.as_view(), name='sales-edit'),
    path('sales/<int:pk>/delete/', views.SalesDeleteView.as_view(), name='sales-delete'),

    # Purchases
    path('purchases/', views.PurchaseListView.as_view(), name='purchases-list'),
    path('purchases/add/', views.PurchaseCreateView.as_view(), name='purchases-add'),
    path('purchases/<int:pk>/edit/', views.PurchaseUpdateView.as_view(), name='purchases-edit'),
    path('purchases/<int:pk>/delete/', views.PurchaseDeleteView.as_view(), name='purchases-delete'),
]
