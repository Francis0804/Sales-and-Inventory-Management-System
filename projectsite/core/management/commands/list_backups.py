# core/management/commands/list_backups.py
from django.core.management.base import BaseCommand
from core.backup import BackupManager
from datetime import datetime

class Command(BaseCommand):
    help = 'List all available database backups'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--stats',
            action='store_true',
            help='Show backup statistics'
        )
    
    def handle(self, *args, **options):
        show_stats = options.get('stats', False)
        
        backups = BackupManager.get_backups()
        
        if not backups:
            self.stdout.write(self.style.WARNING("No backups found."))
            return
        
        self.stdout.write(self.style.SUCCESS(f"\n📦 Available Backups ({len(backups)} total):\n"))
        
        for i, backup in enumerate(backups, 1):
            date_obj = datetime.fromisoformat(backup['datetime'])
            formatted_date = date_obj.strftime('%Y-%m-%d %H:%M:%S')
            
            description = backup.get('description', '')
            desc_str = f" - {description}" if description else ""
            
            self.stdout.write(
                f"{i}. {backup['filename']}\n"
                f"   Date: {formatted_date}\n"
                f"   Size: {backup['size_mb']} MB{desc_str}\n"
            )
        
        if show_stats:
            stats = BackupManager.get_backup_statistics()
            self.stdout.write(self.style.SUCCESS("\n📊 Backup Statistics:\n"))
            self.stdout.write(f"  Total Backups: {stats['total_backups']}")
            self.stdout.write(f"  Total Size: {stats['total_size_mb']} MB")
            self.stdout.write(f"  Latest: {stats['latest_backup']['filename'] if stats['latest_backup'] else 'None'}")
            self.stdout.write(f"  Oldest: {stats['oldest_backup']['filename'] if stats['oldest_backup'] else 'None'}")
