# core/views_backup.py (add to core/views.py)
import json
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import UserRole, AuditLog
from .backup import BackupManager

class AdminRequiredMixin(UserPassesTestMixin):
    """Mixin to require admin role"""
    def test_func(self):
        try:
            return self.request.user.user_role.role == 'admin'
        except UserRole.DoesNotExist:
            return False
    
    def handle_no_permission(self):
        messages.error(self.request, 'You do not have permission to access this page.')
        return redirect('home')

class BackupListView(AdminRequiredMixin, LoginRequiredMixin, ListView):
    """List all backups"""
    template_name = 'backups/backup_list.html'
    context_object_name = 'backups'
    paginate_by = 10
    login_url = 'login'
    
    def get_queryset(self):
        # Return backups as a list (not a queryset)
        return BackupManager.get_backups()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stats'] = BackupManager.get_backup_statistics()
        return context

@login_required(login_url='login')
def create_backup_view(request):
    """Create a new backup"""
    try:
        if request.user.user_role.role != 'admin':
            messages.error(request, 'Only administrators can create backups.')
            return redirect('home')
    except UserRole.DoesNotExist:
        return redirect('home')
    
    if request.method == 'POST':
        description = request.POST.get('description', '')
        result = BackupManager.create_backup(description=description)
        
        if result.get('status') == 'success':
            messages.success(
                request,
                f"Backup created successfully: {result['filename']} ({result['size_mb']} MB)"
            )
            try:
                detail = f"filename={result.get('filename')}; size_mb={result.get('size_mb')}; description={result.get('description','')}"
                AuditLog.objects.create(
                    user=request.user,
                    action='create_backup',
                    target=result.get('filename'),
                    detail=detail
                )
            except Exception:
                pass
        else:
            messages.error(request, f"Backup failed: {result.get('error', 'Unknown error')}")
        
        return redirect('backup-list')
    
    return render(request, 'backups/create_backup.html')

@login_required(login_url='login')
def restore_backup_view(request, backup_filename):
    """Restore from a backup"""
    try:
        if request.user.user_role.role != 'admin':
            messages.error(request, 'Only administrators can restore backups.')
            return redirect('home')
    except UserRole.DoesNotExist:
        return redirect('home')
    
    # Get backup info
    backups = BackupManager.get_backups()
    backup_info = None
    for backup in backups:
        if backup.get('filename') == backup_filename:
            backup_info = backup
            break
    
    if not backup_info:
        messages.error(request, f'Backup not found: {backup_filename}')
        return redirect('backup-list')
    
    if request.method == 'POST':
        confirm = request.POST.get('confirm', 'no')
        
        if confirm == 'yes':
            result = BackupManager.restore_backup(backup_filename)
            
            if result.get('status') == 'success':
                messages.success(request, f"Database restored from {backup_filename}")
                try:
                    AuditLog.objects.create(
                        user=request.user,
                        action='restore_backup',
                        target=backup_filename,
                        detail=f"restored={result.get('status')}; message={result.get('message','')}"
                    )
                except Exception:
                    pass
            else:
                messages.error(request, f"Restoration failed: {result.get('error')}")
        else:
            messages.warning(request, 'Restoration cancelled.')
        
        return redirect('backup-list')
    
    return render(request, 'backups/restore_backup.html', {
        'backup': backup_info,
        'backup_filename': backup_filename
    })

@login_required(login_url='login')
def delete_backup_view(request, backup_filename):
    """Delete a backup"""
    try:
        if request.user.user_role.role != 'admin':
            messages.error(request, 'Only administrators can delete backups.')
            return redirect('home')
    except UserRole.DoesNotExist:
        return redirect('home')
    
    if request.method == 'POST':
        confirm = request.POST.get('confirm', 'no')
        
        if confirm == 'yes':
            result = BackupManager.delete_backup(backup_filename)
            
            if result.get('status') == 'success':
                messages.success(request, f"Backup {backup_filename} deleted")
                try:
                    AuditLog.objects.create(
                        user=request.user,
                        action='delete_backup',
                        target=backup_filename,
                        detail=f"deleted={result.get('status')}; message={result.get('message','')}"
                    )
                except Exception:
                    pass
            else:
                messages.error(request, f"Deletion failed: {result.get('error')}")
        else:
            messages.warning(request, 'Deletion cancelled.')
        
        return redirect('backup-list')
    
    # Get backup info for confirmation
    backups = BackupManager.get_backups()
    backup_info = None
    for backup in backups:
        if backup.get('filename') == backup_filename:
            backup_info = backup
            break
    
    return render(request, 'backups/delete_backup.html', {
        'backup': backup_info,
        'backup_filename': backup_filename
    })

@login_required(login_url='login')
def cleanup_backups_view(request):
    """Cleanup old backups"""
    try:
        if request.user.user_role.role != 'admin':
            messages.error(request, 'Only administrators can cleanup backups.')
            return redirect('home')
    except UserRole.DoesNotExist:
        return redirect('home')
    
    if request.method == 'POST':
        days = int(request.POST.get('days', 30))
        result = BackupManager.cleanup_old_backups(days=days)
        
        if result.get('status') == 'success':
            messages.success(
                request,
                f"Cleanup completed: Deleted {result['deleted_count']} backups, "
                f"Freed {result['freed_space_mb']} MB"
            )
            try:
                detail = f"deleted_count={result.get('deleted_count')}; freed_space_mb={result.get('freed_space_mb')}"
                AuditLog.objects.create(
                    user=request.user,
                    action='cleanup_backups',
                    target='backups_cleanup',
                    detail=detail
                )
            except Exception:
                pass
        else:
            messages.error(request, f"Cleanup failed: {result.get('error')}")
        
        return redirect('backup-list')
    
    return render(request, 'backups/cleanup_backups.html')
