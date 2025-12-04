# core/fields.py
from django.db import models
from .encryption import EncryptionManager

class EncryptedCharField(models.CharField):
    """CharField that automatically encrypts/decrypts values"""
    
    def from_db_value(self, value, expression, connection):
        """Decrypt value when reading from database"""
        if value is None:
            return value
        return EncryptionManager.decrypt(value)
    
    def get_prep_value(self, value):
        """Encrypt value before saving to database"""
        if value is None:
            return value
        return EncryptionManager.encrypt(value)

class EncryptedEmailField(models.EmailField):
    """EmailField that automatically encrypts/decrypts values"""
    
    def from_db_value(self, value, expression, connection):
        """Decrypt value when reading from database"""
        if value is None:
            return value
        return EncryptionManager.decrypt(value)
    
    def get_prep_value(self, value):
        """Encrypt value before saving to database"""
        if value is None:
            return value
        return EncryptionManager.encrypt(value)

class EncryptedTextField(models.TextField):
    """TextField that automatically encrypts/decrypts values"""
    
    def from_db_value(self, value, expression, connection):
        """Decrypt value when reading from database"""
        if value is None:
            return value
        return EncryptionManager.decrypt(value)
    
    def get_prep_value(self, value):
        """Encrypt value before saving to database"""
        if value is None:
            return value
        return EncryptionManager.encrypt(value)
