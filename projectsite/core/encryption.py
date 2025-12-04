# core/encryption.py
from cryptography.fernet import Fernet
from django.conf import settings
import base64
import hashlib

class EncryptionManager:
    """Manage encryption/decryption of sensitive fields"""
    
    @staticmethod
    def get_cipher():
        """Get Fernet cipher with key from settings"""
        # Generate a key from Django SECRET_KEY if not provided
        if hasattr(settings, 'ENCRYPTION_KEY'):
            key = settings.ENCRYPTION_KEY
        else:
            # Generate deterministic key from SECRET_KEY
            hash_obj = hashlib.sha256(settings.SECRET_KEY.encode())
            key = base64.urlsafe_b64encode(hash_obj.digest())
        
        return Fernet(key)
    
    @staticmethod
    def encrypt(value):
        """
        Encrypt a string value
        
        Args:
            value: String to encrypt
            
        Returns:
            str: Encrypted value
        """
        if not value:
            return value
        
        try:
            cipher = EncryptionManager.get_cipher()
            encrypted = cipher.encrypt(str(value).encode())
            return encrypted.decode()
        except Exception as e:
            print(f"Encryption error: {e}")
            return value
    
    @staticmethod
    def decrypt(encrypted_value):
        """
        Decrypt an encrypted value
        
        Args:
            encrypted_value: Encrypted string
            
        Returns:
            str: Decrypted value
        """
        if not encrypted_value:
            return encrypted_value
        
        try:
            cipher = EncryptionManager.get_cipher()
            decrypted = cipher.decrypt(encrypted_value.encode())
            return decrypted.decode()
        except Exception as e:
            print(f"Decryption error: {e}")
            return encrypted_value
    
    @staticmethod
    def generate_encryption_key():
        """Generate a new encryption key"""
        return Fernet.generate_key().decode()
