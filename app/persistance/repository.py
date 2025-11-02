from app.models.base_model import db
from sqlalchemy.exc import SQLAlchemyError


class SQLAlchemyRepository:
    """Generic repository for any SQLAlchemy model"""

    def __init__(self, model):
        self.model = model

    def get_by_id(self, id):
        """Retrieve an obj by ID"""
        return self.model.query.get(id)
    
    def get_all(self):
        """Retrieve all obj of the model"""
        return self.model.query.all()
    
    def save(self, obj):
        """Save an obj in DB"""
        try:
            db.session.add(obj)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollbacl()
            raise e
        
    def delele(self, obj):
        """Delete an obj of the DB"""
        try:
            db.session.delete(obj)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
