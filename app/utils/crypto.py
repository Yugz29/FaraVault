from cryptography.fernet import Fernet

def generate_key():
    """Generate a new Fernet key"""
    return Fernet.generate_key()

def encrypt(value: str, key: bytes) -> str:
    """Encrypt a string value using the provided Fernet key"""
    f = Fernet(key)
    return f.encrypt(value.encode()).decode()

def decrypt(token: str, key: bytes) -> str:
    """Decrypt a string token using the provided Fernet key"""
    f = Fernet(key)
    return f.decrypt(token.encode()).decode()
