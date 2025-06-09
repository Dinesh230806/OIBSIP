from cryptography.fernet import Fernet

class EncryptionManager:
    def __init__(self):
        self.key = b'CdkW6E-EpEDi3B_fI3NKFrjZEG3FyhM3kyehQ2kuU5c='  # MUST have b prefix
        self.cipher = Fernet(self.key)

    def encrypt(self, message):
        if isinstance(message, str):
            message = message.encode('utf-8')
        return self.cipher.encrypt(message)

    def decrypt(self, encrypted_message):
        if isinstance(encrypted_message, str):
            encrypted_message = encrypted_message.encode('utf-8')
        return self.cipher.decrypt(encrypted_message).decode('utf-8')