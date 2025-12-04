# core/backup.py
import json
import gzip
import os
from datetime import datetime
from pathlib import Path
from django.db import connection
from django.core.management import call_command
from django.conf import settings
import sqlite3
import shutil

class BackupManager:
    """Manage database backups and recovery"""
    
    BACKUP_DIR = Path(settings.BASE_DIR) / 'backups'
    
    def __init__(self):
        """Initialize backup directory"""
        self.BACKUP_DIR.mkdir(exist_ok=True)
    
    @staticmethod
    def get_backup_path(timestamp=None):
        """Generate backup file path"""
        if timestamp is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return BackupManager.BACKUP_DIR / f'backup_{timestamp}.db.gz'
    
    @staticmethod
    def create_backup(description=""):
        """
        Create a complete database backup
        
        Args:
            description: Optional description for the backup
            
        Returns:
            dict: Backup metadata {filename, path, size, timestamp, description}
        """
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = BackupManager.get_backup_path(timestamp)
            
            # Ensure backup directory exists
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Get current database file
            db_path = settings.DATABASES['default']['NAME']
            
            # Create gzip compressed backup
            with open(db_path, 'rb') as f_in:
                with gzip.open(backup_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            
            # Get file size
            file_size = backup_path.stat().st_size
            
            # Store metadata
            metadata = {
                'filename': backup_path.name,
                'path': str(backup_path),
                'size': file_size,
                'size_mb': round(file_size / (1024 * 1024), 2),
                'timestamp': timestamp,
                'datetime': datetime.now().isoformat(),
                'description': description,
                'status': 'success'
            }
            
            # Save metadata to JSON
            metadata_path = backup_path.with_suffix('.json')
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            return metadata
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    @staticmethod
    def get_backups():
        """
        Get list of all available backups
        
        Returns:
            list: Sorted list of backup metadata
        """
        backups = []
        backup_dir = BackupManager.BACKUP_DIR
        
        if not backup_dir.exists():
            return backups
        
        # Find all .json metadata files
        for metadata_file in sorted(backup_dir.glob('backup_*.json'), reverse=True):
            try:
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                    backups.append(metadata)
            except Exception as e:
                print(f"Error reading metadata {metadata_file}: {e}")
        
        return backups
    
    @staticmethod
    def restore_backup(backup_filename):
        """
        Restore database from backup
        
        Args:
            backup_filename: Name of backup file (e.g., 'backup_20251204_120000.db.gz')
            
        Returns:
            dict: Restoration result
        """
        try:
            backup_path = BackupManager.BACKUP_DIR / backup_filename
            
            # Verify backup exists
            if not backup_path.exists():
                return {
                    'status': 'error',
                    'error': f'Backup file not found: {backup_filename}'
                }
            
            # Get current database path
            db_path = settings.DATABASES['default']['NAME']
            
            # Create a restore point backup before restoring
            restore_point = BackupManager.get_backup_path(
                datetime.now().strftime('%Y%m%d_%H%M%S_restore_point')
            )
            with open(db_path, 'rb') as f_in:
                with gzip.open(restore_point, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            
            # Restore from backup
            with gzip.open(backup_path, 'rb') as f_in:
                with open(db_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            
            return {
                'status': 'success',
                'message': f'Database restored from {backup_filename}',
                'restore_point': restore_point.name,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    @staticmethod
    def delete_backup(backup_filename):
        """
        Delete a backup file
        
        Args:
            backup_filename: Name of backup file to delete
            
        Returns:
            dict: Deletion result
        """
        try:
            backup_path = BackupManager.BACKUP_DIR / backup_filename
            metadata_path = backup_path.with_suffix('.json')
            
            # Delete backup file
            if backup_path.exists():
                backup_path.unlink()
            
            # Delete metadata file
            if metadata_path.exists():
                metadata_path.unlink()
            
            return {
                'status': 'success',
                'message': f'Backup {backup_filename} deleted',
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    @staticmethod
    def get_backup_statistics():
        """
        Get backup statistics
        
        Returns:
            dict: Statistics about backups
        """
        backups = BackupManager.get_backups()
        total_size = sum(b.get('size', 0) for b in backups)
        
        return {
            'total_backups': len(backups),
            'total_size_bytes': total_size,
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'latest_backup': backups[0] if backups else None,
            'oldest_backup': backups[-1] if backups else None
        }
    
    @staticmethod
    def cleanup_old_backups(days=30):
        """
        Delete backups older than specified days
        
        Args:
            days: Number of days to keep backups
            
        Returns:
            dict: Cleanup result
        """
        try:
            from datetime import timedelta
            
            cutoff_date = datetime.now() - timedelta(days=days)
            deleted_count = 0
            freed_space = 0
            
            backup_dir = BackupManager.BACKUP_DIR
            for backup_file in backup_dir.glob('backup_*.db.gz'):
                try:
                    # Parse timestamp from filename
                    timestamp_str = backup_file.name.split('_')[1:3]
                    timestamp_str = '_'.join(timestamp_str).replace('.db.gz', '')
                    backup_date = datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')
                    
                    if backup_date < cutoff_date:
                        freed_space += backup_file.stat().st_size
                        backup_file.unlink()
                        
                        # Also delete metadata file
                        metadata_file = backup_file.with_suffix('.json')
                        if metadata_file.exists():
                            metadata_file.unlink()
                        
                        deleted_count += 1
                except Exception as e:
                    print(f"Error processing backup {backup_file}: {e}")
            
            return {
                'status': 'success',
                'deleted_count': deleted_count,
                'freed_space_mb': round(freed_space / (1024 * 1024), 2),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
