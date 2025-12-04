# core/settings_backup.py
"""
Backup and Security Configuration

Add to your main settings.py:

# Backup Configuration
from core.settings_backup import *

# Or manually add:
BACKUP_DIR = os.path.join(BASE_DIR, 'backups')
BACKUP_RETENTION_DAYS = 30
AUTO_BACKUP_ENABLED = True
AUTO_BACKUP_TIME = '02:00'  # 2 AM daily

# Encryption Configuration
ENCRYPTION_ENABLED = True
# Generate a key with: python manage.py generate_encryption_key
# ENCRYPTION_KEY = b'your-encryption-key-here'
"""

import os
from django.conf import settings

# Backup Configuration
BACKUP_DIR = os.path.join(settings.BASE_DIR, 'backups')
BACKUP_RETENTION_DAYS = 30  # Keep backups for 30 days
AUTO_BACKUP_ENABLED = True  # Enable automatic backups
AUTO_BACKUP_TIME = '02:00'  # 2 AM UTC daily

# Create backups directory if it doesn't exist
os.makedirs(BACKUP_DIR, exist_ok=True)

# Encryption Configuration
ENCRYPTION_ENABLED = True

# Sensitive fields to encrypt
ENCRYPTED_FIELDS = {
    'Product': ['unit_price'],
    'Supplier': ['email', 'phone', 'address'],
    'PurchaseOrder': ['total_amount', 'total_subtotal', 'total_tax'],
}
