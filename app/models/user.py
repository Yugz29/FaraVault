from app import db, BaseModel
from werkzeug.security import generate_password_hash, check_password_hash


class User(BaseModel):
    __tablename__ = 'users'

    """Columns"""
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    """Relationships"""
    secrets = db.relationship('Secret', back_populates='user', lazy='select')

    """Password methods"""
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    """Dictonary representation"""
    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "email": self.email,
            "is_admin": self.is_admin
        })
        return base_dict
    
    def __repr__(self):
        return f"<User {self.first_name} {self.last_name} {self.username} ({self.email})>"
