from app.models.api import API
from app.models.user import User
from app.persistance.repository import SQLAlchemyRepository
from app.persistance.repositories.user_repository import UserRepository
from app.utils.crypto import encrypt, decrypt, generate_key



class FaraVault:
    def __init__(self):
        self.user_repo = UserRepository()
        self.api_repo = SQLAlchemyRepository(API)
        
    """API methods"""
    def create_api(self, user, data):
        """Create a new API"""
        if 'name' not in data or not data['name']:
            raise ValueError("API name is required")
        name = data['name']
        description = data.get('description')
        api = API(name=name, description=description, user=user)
        encryption_key = user.get_encryption_key()
        if 'secret_key' in data and data['secret_key']:
            api.secret_key = encrypt(data['secret_key'], encryption_key)
        if 'public_key' in data and data['public_key']:
            api.public_key = encrypt(data['public_key'], encryption_key)
        self.api_repo.save(api)
        return api

    def get_all_apis(self, user):
        """Retrieve all API of the user"""
        pass

    def get_api_by_id(self, user, api_id):
        """Retrieve an precise API"""
        pass