# core/management/commands/restore_backup.py
from django.core.management.base import BaseCommand
from core.backup import BackupManager

class Command(BaseCommand):
    help = 'Restore database from a backup'
    
    def add_arguments(self, parser):
        parser.add_argument(
            'backup_file',
            type=str,
            help='Name of the backup file to restore (e.g., backup_20251204_120000.db.gz)'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Skip confirmation prompt'
        )
    
    def handle(self, *args, **options):
        backup_file = options['backup_file']
        force = options.get('force', False)
        
        # Get backup info
        backups = BackupManager.get_backups()
        backup_info = None
        for backup in backups:
            if backup.get('filename') == backup_file:
                backup_info = backup
                break
        
        if not backup_info:
            self.stdout.write(
                self.style.ERROR(f"✗ Backup not found: {backup_file}")
            )
            self.stdout.write(self.style.WARNING("\nAvailable backups:"))
            for backup in backups:
                print(f"  - {backup['filename']} ({backup['size_mb']} MB)")
            return
        
        # Confirm restoration
        if not force:
            self.stdout.write(self.style.WARNING(
                f"\n⚠️  WARNING: This will restore your database from {backup_file}\n"
                f"   Date: {backup_info['datetime']}\n"
                f"   Size: {backup_info['size_mb']} MB\n"
                f"   Description: {backup_info.get('description', 'None')}"
            ))
            confirm = input("\nAre you sure you want to restore? (yes/no): ").lower()
            if confirm != 'yes':
                self.stdout.write(self.style.WARNING("Restoration cancelled."))
                return
        
        # Restore backup
        self.stdout.write(self.style.SUCCESS('\nRestoring backup...'))
        result = BackupManager.restore_backup(backup_file)
        
        if result.get('status') == 'success':
            self.stdout.write(
                self.style.SUCCESS(
                    f"✓ Database restored successfully!\n"
                    f"  Message: {result['message']}\n"
                    f"  Restore Point: {result['restore_point']}"
                )
            )
        else:
            self.stdout.write(
                self.style.ERROR(f"✗ Restoration failed: {result.get('error', 'Unknown error')}")
            )
