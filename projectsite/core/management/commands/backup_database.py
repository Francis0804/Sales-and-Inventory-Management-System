# core/management/commands/backup_database.py
from django.core.management.base import BaseCommand
from core.backup import BackupManager

class Command(BaseCommand):
    help = 'Create a database backup'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--description',
            type=str,
            default='',
            help='Optional description for the backup'
        )
        parser.add_argument(
            '--cleanup',
            type=int,
            default=0,
            help='Delete backups older than X days (0 = no cleanup)'
        )
    
    def handle(self, *args, **options):
        description = options.get('description', '')
        cleanup_days = options.get('cleanup', 0)
        
        # Create backup
        self.stdout.write(self.style.SUCCESS('Creating backup...'))
        result = BackupManager.create_backup(description=description)
        
        if result.get('status') == 'success':
            self.stdout.write(
                self.style.SUCCESS(
                    f"✓ Backup created successfully!\n"
                    f"  File: {result['filename']}\n"
                    f"  Size: {result['size_mb']} MB\n"
                    f"  Location: {result['path']}"
                )
            )
        else:
            self.stdout.write(
                self.style.ERROR(f"✗ Backup failed: {result.get('error', 'Unknown error')}")
            )
            return
        
        # Cleanup old backups if requested
        if cleanup_days > 0:
            self.stdout.write(self.style.SUCCESS(f'\nCleaning up backups older than {cleanup_days} days...'))
            cleanup_result = BackupManager.cleanup_old_backups(days=cleanup_days)
            
            if cleanup_result.get('status') == 'success':
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✓ Cleanup completed!\n"
                        f"  Deleted: {cleanup_result['deleted_count']} backups\n"
                        f"  Freed: {cleanup_result['freed_space_mb']} MB"
                    )
                )
