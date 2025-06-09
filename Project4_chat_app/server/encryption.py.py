import os
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import logging
from typing import Union, Optional, Dict, Any
from getpass import getpass

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EncryptionManager:
    # Development key - override with environment variable in production
    DEFAULT_KEY = b'CdkW6E-EpEDi3B_fI3NKFrjZEG3FyhM3kyehQ2kuU5c='
    
    def __init__(self, key: Optional[bytes] = None, key_env_var: str = "CHAT_APP_SECRET_KEY"):
        """Initialize encryption manager with key from either:
        - Provided key parameter
        - Environment variable
        - Default development key
        
        Args:
            key: Optional direct key input
            key_env_var: Environment variable name to check for key
        """
        self.key = self._load_key(key, key_env_var)
        self.cipher = Fernet(self.key)
        logger.info("Encryption manager initialized with %s key source", 
                   "provided" if key else "environment" if os.getenv(key_env_var) else "default")

    def _load_key(self, provided_key: Optional[bytes], env_var: str) -> bytes:
        """Load key with fallback hierarchy:
        1. Provided key parameter
        2. Environment variable
        3. Default development key
        
        Raises:
            ValueError: If no valid key found in production mode
        """
        # 1. Check provided key
        if provided_key is not None:
            if self._validate_key(provided_key):
                return provided_key
            raise ValueError("Invalid provided encryption key")

        # 2. Check environment variable
        env_key = os.getenv(env_var)
        if env_key:
            try:
                key_bytes = base64.urlsafe_b64decode(env_key)
                if self._validate_key(key_bytes):
                    return key_bytes
            except (ValueError, TypeError) as e:
                logger.warning("Invalid key in environment variable: %s", str(e))

        # 3. Use default key in development only
        if os.getenv("FLASK_ENV") == "development":
            logger.warning("Using default development key - NOT SAFE FOR PRODUCTION")
            return self.DEFAULT_KEY

        raise ValueError(
            f"No valid encryption key found. "
            f"Set {env_var} environment variable with base64-encoded Fernet key"
        )

    @staticmethod
    def _validate_key(key: bytes) -> bool:
        """Validate Fernet key format."""
        try:
            Fernet(key)
            return True
        except (ValueError, TypeError):
            return False

    def encrypt(self, message: Union[str, bytes]) -> bytes:
        """Encrypt message with proper type checking."""
        if not message:
            raise ValueError("Cannot encrypt empty message")
            
        message_bytes = message.encode('utf-8') if isinstance(message, str) else message
        if not isinstance(message_bytes, bytes):
            raise TypeError("Message must be str or bytes")

        try:
            return self.cipher.encrypt(message_bytes)
        except Exception as e:
            logger.error("Encryption failed: %s", str(e))
            raise

    def decrypt(self, encrypted_message: Union[str, bytes]) -> str:
        """Decrypt message with comprehensive error handling."""
        try:
            if isinstance(encrypted_message, str):
                encrypted_message = base64.urlsafe_b64decode(encrypted_message)
            
            if not isinstance(encrypted_message, bytes):
                raise TypeError("Encrypted message must be str or bytes")
                
            return self.cipher.decrypt(encrypted_message).decode('utf-8')
        except InvalidToken as e:
            logger.warning("Decryption failed - invalid token")
            raise
        except Exception as e:
            logger.error("Decryption error: %s", str(e))
            raise

    # Additional utility methods remain unchanged...
    # (generate_key_from_password, generate_new_key, encrypt_dict, decrypt_dict, etc.)

    @classmethod
    def initialize_for_development(cls) -> 'EncryptionManager':
        """Convenience method for development setup."""
        logger.warning("Initializing with development key - FOR TESTING ONLY")
        return cls(key=cls.DEFAULT_KEY)