from cryptography.fernet import Fernet
print("Generated key:", Fernet.generate_key().decode())
input("Press Enter to exit...")