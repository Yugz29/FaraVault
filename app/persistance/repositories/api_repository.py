from app.models.api import API
from app.persistance.repository import SQLAlchemyRepository

class APIRepository(SQLAlchemyRepository):
    """Repository specific to APIs"""

    def __init__(self):
        super().__init__(API)

    def get_api_by_name(self, name):
        """Returns an API by its name"""
        return self.model.query.filter_by(name=name).first()
