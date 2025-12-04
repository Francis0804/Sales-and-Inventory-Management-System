from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from core import views
from core.views_backup import (
    BackupListView, create_backup_view, restore_backup_view, 
    delete_backup_view, cleanup_backups_view
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Home
    path('', views.home, name='home'),
    
    # Login & Logout
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit-profile'),

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

    # Purchases
    path('purchases/', views.PurchaseListView.as_view(), name='purchases-list'),
    path('purchases/add/', views.PurchaseCreateView.as_view(), name='purchases-add'),
    path('purchases/<int:pk>/', views.PurchaseDetailView.as_view(), name='purchases-detail'),
    path('purchases/<int:pk>/edit/', views.PurchaseUpdateView.as_view(), name='purchases-edit'),
    path('purchases/<int:pk>/delete/', views.PurchaseDeleteView.as_view(), name='purchases-delete'),

    # Reports & Analytics
    path('reports/', views.ReportsView.as_view(), name='reports-dashboard'),
    path('reports/inventory/', views.inventory_report, name='inventory-report'),
    path('reports/fast-moving/', views.fast_moving_report, name='fast-moving-report'),
    path('reports/profit-loss/', views.profit_loss_report, name='profit-loss-report'),
    path('reports/export/excel/', views.export_report_excel, name='export-excel'),

    # User Management
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    path('users/<int:user_id>/assign-role/', views.assign_user_role, name='assign-role'),

    # Backup & Recovery
    path('backups/', BackupListView.as_view(), name='backup-list'),
    path('backups/create/', create_backup_view, name='backup-create'),
    path('backups/<str:backup_filename>/restore/', restore_backup_view, name='backup-restore'),
    path('backups/<str:backup_filename>/delete/', delete_backup_view, name='backup-delete'),
    path('backups/cleanup/', cleanup_backups_view, name='backup-cleanup'),
    # Audit logs (admin)
    path('audit-logs/', views.AuditLogListView.as_view(), name='audit-log-list'),
]
