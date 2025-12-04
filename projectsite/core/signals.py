import json
from datetime import date, datetime
from django.db.models.signals import pre_save, post_save, post_delete
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.utils import timezone
from .models import (
    AuditLog, Product, Supplier, Category, PurchaseOrder, PurchaseItem
)
from .middleware import get_current_user

# Simple in-memory cache to hold pre-save snapshots for change detection
_PRE_SAVE_CACHE = {}

def _snapshot_instance(instance):
    data = {}
    for f in instance._meta.fields:
        # Exclude audit timestamp fields from snapshot details
        if f.name in ('created_at', 'updated_at'):
            continue
        try:
            data[f.name] = getattr(instance, f.name)
        except Exception:
            data[f.name] = None
    return data


def _format_snapshot(snapshot: dict) -> str:
    parts = []
    for k, v in snapshot.items():
        # Skip any datetime/date values to avoid showing timestamps in details
        if isinstance(v, (date, datetime)):
            continue
        parts.append(f"{k}={v}")
    return '; '.join(parts)


def _format_changes(changes: list) -> str:
    parts = []
    for ch in changes:
        field = ch.get('field')
        # Skip created_at/updated_at changes to avoid date noise in detail
        if field in ('created_at', 'updated_at'):
            continue
        old = ch.get('old')
        new = ch.get('new')
        # Skip if old/new are date/datetime values
        if isinstance(old, (date, datetime)) or isinstance(new, (date, datetime)):
            continue
        parts.append(f"{field}: {old} -> {new}")
    return '; '.join(parts)

def _create_audit(user, action, target, detail=""):
    try:
        AuditLog.objects.create(user=user, action=action, target=target, detail=str(detail))
    except Exception:
        # Fail silently; auditing should not break main flow
        pass


def _register_pre_save(sender, instance, **kwargs):
    if instance.pk:
        try:
            orig = sender.objects.get(pk=instance.pk)
            _PRE_SAVE_CACHE[(sender, instance.pk)] = _snapshot_instance(orig)
        except sender.DoesNotExist:
            pass


def _register_post_save(sender, instance, created, **kwargs):
    user = get_current_user()
    target = f"{sender.__name__}:{getattr(instance, 'pk', None)}"
    if created:
        # Friendly, non-technical create messages (no datetimes)
        if sender.__name__ == 'Supplier':
            name = getattr(instance, 'name', None)
            detail = f"Supplier '{name}' was created"
        elif sender.__name__ == 'Category':
            name = getattr(instance, 'name', None)
            detail = f"Category '{name}' was created"
        elif sender.__name__ == 'Product':
            try:
                code = getattr(instance, 'code', None)
                name = getattr(instance, 'name', None)
                label = f"({code})_{name}"
                detail = f"Product '{label}' was created"
            except Exception:
                detail = "Product was created"
        elif sender.__name__ == 'PurchaseOrder':
            detail = f"Purchase order #{getattr(instance, 'pk', '')} was created"
        elif sender.__name__ == 'PurchaseItem':
            detail = "Purchase item was added"
        else:
            snapshot = _snapshot_instance(instance)
            detail = _format_snapshot(snapshot)
        _create_audit(user, 'created', target, detail)
        # If a new product is created with zero quantity, log as out of stock
        if sender.__name__ == 'Product':
            try:
                qty = int(getattr(instance, 'quantity', 0) or 0)
                if qty == 0:
                    try:
                        code = getattr(instance, 'code', None)
                        name = getattr(instance, 'name', None)
                        label = f"({code})_{name}"
                        _create_audit(user, 'created_out_of_stock', target, f"{label} - quantity={qty} (out of stock)")
                    except Exception:
                        _create_audit(user, 'created_out_of_stock', target, f'quantity={qty} (out of stock)')
            except Exception:
                pass
    else:
        old = _PRE_SAVE_CACHE.pop((sender, instance.pk), None) or {}
        new = _snapshot_instance(instance)
        changes = []
        for k, v in new.items():
            oldv = old.get(k)
            if str(oldv) != str(v):
                changes.append({'field': k, 'old': oldv, 'new': v})
        if changes:
            # Produce non-technical update message
            if sender.__name__ == 'Supplier':
                name = getattr(instance, 'name', None)
                detail = f"Supplier '{name}' was updated"
            elif sender.__name__ == 'Category':
                name = getattr(instance, 'name', None)
                detail = f"Category '{name}' was updated"
            elif sender.__name__ == 'Product':
                try:
                    code = getattr(instance, 'code', None)
                    name = getattr(instance, 'name', None)
                    label = f"({code})_{name}"
                    detail = f"Product '{label}' was updated"
                except Exception:
                    detail = "Product was updated"
            else:
                detail = f"{sender.__name__} was updated"
            _create_audit(user, 'updated', target, detail)
            # Quantity-specific audit: detect restock or out-of-stock
            for ch in changes:
                if ch.get('field') == 'quantity':
                    try:
                        old_q = int(ch.get('old') or 0)
                        new_q = int(ch.get('new') or 0)
                        if new_q > old_q:
                            # Friendly restocked message
                            if sender.__name__ == 'Product':
                                try:
                                    code = getattr(instance, 'code', None)
                                    name = getattr(instance, 'name', None)
                                    label = f"({code})_{name}"
                                    _create_audit(user, 'restocked', target, f"Product '{label}' was restocked from {old_q} to {new_q}")
                                except Exception:
                                    _create_audit(user, 'restocked', target, f'Product was restocked from {old_q} to {new_q}')
                            else:
                                _create_audit(user, 'restocked', target, f'Item was restocked from {old_q} to {new_q}')
                        if new_q == 0:
                            if sender.__name__ == 'Product':
                                try:
                                    code = getattr(instance, 'code', None)
                                    name = getattr(instance, 'name', None)
                                    label = f"({code})_{name}"
                                    _create_audit(user, 'marked_out_of_stock', target, f"Product '{label}' is out of stock")
                                except Exception:
                                    _create_audit(user, 'marked_out_of_stock', target, f'Product is out of stock')
                            else:
                                _create_audit(user, 'marked_out_of_stock', target, f'Item is out of stock')
                    except Exception:
                        pass


def _register_post_delete(sender, instance, **kwargs):
    user = get_current_user()
    target = f"{sender.__name__}:{getattr(instance, 'pk', None)}"
    # Friendly delete messages
    if sender.__name__ == 'Supplier':
        name = getattr(instance, 'name', None)
        detail = f"Supplier '{name}' was deleted"
    elif sender.__name__ == 'Category':
        name = getattr(instance, 'name', None)
        detail = f"Category '{name}' was deleted"
    elif sender.__name__ == 'Product':
        try:
            code = getattr(instance, 'code', None)
            name = getattr(instance, 'name', None)
            label = f"({code})_{name}"
            detail = f"Product '{label}' was deleted"
        except Exception:
            detail = "Product was deleted"
    elif sender.__name__ == 'PurchaseOrder':
        detail = f"Purchase order #{getattr(instance, 'pk', '')} was deleted"
    elif sender.__name__ == 'PurchaseItem':
        detail = "Purchase item was removed"
    else:
        snapshot = _snapshot_instance(instance)
        detail = _format_snapshot(snapshot)
    _create_audit(user, 'deleted', target, detail)


# Attach handlers for models we want to audit
for model in (Product, Supplier, Category, PurchaseOrder, PurchaseItem):
    pre_save.connect(_register_pre_save, sender=model)
    post_save.connect(_register_post_save, sender=model)
    post_delete.connect(_register_post_delete, sender=model)


# User activity signals
@receiver(user_logged_in)
def _user_logged_in(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR') or request.META.get('HTTP_X_FORWARDED_FOR') or 'unknown'
    uname = getattr(user, 'username', 'Unknown')
    detail = f"User '{uname}' logged in from {ip}"
    _create_audit(user, 'login', f'User:{user.pk}', detail)


@receiver(user_logged_out)
def _user_logged_out(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR') or request.META.get('HTTP_X_FORWARDED_FOR') or 'unknown'
    uname = getattr(user, 'username', 'Unknown') if user else 'Unknown'
    detail = f"User '{uname}' logged out from {ip}"
    _create_audit(user, 'logout', f'User:{getattr(user, "pk", None)}', detail)
# core/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserRole


@receiver(post_save, sender=User)
def create_user_role(sender, instance, created, **kwargs):
    """Auto-create UserRole when a new User is created"""
    if created:
        # Make superusers/admins get the 'admin' role by default
        default_role = 'admin' if getattr(instance, 'is_superuser', False) or getattr(instance, 'is_staff', False) else 'cashier'
        UserRole.objects.get_or_create(
            user=instance,
            defaults={'role': default_role}
        )


@receiver(post_save, sender=User)
def save_user_role(sender, instance, **kwargs):
    """Save UserRole when User is saved"""
    try:
        instance.user_role.save()
    except UserRole.DoesNotExist:
        # If the user is staff/superuser, create as admin, otherwise cashier
        role = 'admin' if getattr(instance, 'is_superuser', False) or getattr(instance, 'is_staff', False) else 'cashier'
        UserRole.objects.create(user=instance, role=role)


@receiver(post_save, sender=User)
def audit_user_created(sender, instance, created, **kwargs):
    """Create a human-friendly audit entry when a User is created.

    - If created by an authenticated user (admin), record who created it.
    - If created while request user is anonymous, assume registration form.
    - If no request context and user is superuser/staff, assume createsuperuser.
    """
    if not created:
        return

    try:
        current = get_current_user()
        uname = getattr(instance, 'username', 'Unknown')
        if current is None:
            # No request context (likely management command)
            if getattr(instance, 'is_superuser', False) or getattr(instance, 'is_staff', False):
                detail = f"User '{uname}' was created via createsuperuser"
            else:
                detail = f"User '{uname}' was created programmatically"
            _create_audit(None, 'created', f'User:{instance.pk}', detail)
        else:
            # There is a request context
            try:
                if getattr(current, 'is_authenticated', False):
                    detail = f"User '{uname}' was created by '{current.username}'"
                    _create_audit(current, 'created', f'User:{instance.pk}', detail)
                else:
                    # Anonymous request — registration form
                    detail = f"User '{uname}' was created via registration form"
                    _create_audit(None, 'created', f'User:{instance.pk}', detail)
            except Exception:
                # Fallback
                _create_audit(None, 'created', f'User:{instance.pk}', f"User '{uname}' was created")
    except Exception:
        pass
