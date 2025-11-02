from app import db, BaseModel
from app.utils.crypto import encrypt, decrypt
from cryptography.fernet import InvalidToken


class API(BaseModel):
    __tablename__ = "secrets"

    """Columns"""
    name = db.Column(db.String(60), nullable=False)
    description = db.Column(db.Text, nullable=True)
    encrypted_public_key = db.Column(db.String(255), nullable=True, unique=True)
    encrypted_secret_key = db.Column(db.String(255), nullable=True, unique=True)
    user_id = db.Column(db.String(128), db.ForeignKey('users.id'), nullable=False)

    """Relationship"""
    user = db.relationship('User', back_populates='apis')

    """Encrypt methods"""
    def set_secret_key(self, value, key):
        """Encrypt and set the secret key."""
        self.encrypted_secret_key = encrypt(value, key)

    """Decrypt and get the secret key."""
    def get_secret_key(self, key):
        try:
            return decrypt(self.encrypted_secret_key, key)
        except InvalidToken:
            print("Error : Incorrect decryption key")
            return None

    """Encrypt and set the public key."""
    def set_public_key(self, value, key):
        self.encrypted_public_key = encrypt(value, key)

    """Decrypt and get the public key."""
    def get_public_key(self, key):
        try:
            return decrypt(self.encrypted_public_key, key)
        except InvalidToken:
            print("Error : Incorrect decryption key")
            return None
