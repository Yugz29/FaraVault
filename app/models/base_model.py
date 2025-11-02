from app import db
from datetime import datetime
import uuid


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def save(self):
        """Update the 'updated_at' timestamp when the object is modified and save to the database."""
        self.updated_at = datetime.utcnow()
        db.session.add(self)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error saving {self}: {e}")
            raise e
    
    def update_from_dict(self, data: dict):
        forbidden_keys = {'id', 'created_at', 'updated_at'}
        for key, value in data.items():
            if key in forbidden_keys:
                continue
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()

    def to_dict(self):
        """Convert the object to a dictionary representation."""
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id}>"
