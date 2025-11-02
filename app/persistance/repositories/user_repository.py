from app.models.user import User
from app.models.base_model import db
from sqlalchemy.exc import SQLAlchemyError
from app.persistance.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(User)

    def get_user_by_email(self, email):
        return self.model.query.filter_by(email=email).first()
