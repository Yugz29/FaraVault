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
        all_apis = self.api_repo.get_all()
        filtered = [api for api in all_apis if api.user_id == user.id]
        return filtered

    def get_api_by_id(self, user, api_id):
        """Retrieve an precise API"""
        api = self.api_repo.get_by_id(api_id)
        if not api or api.user_id != user.id:
            raise ValueError('API not found or unauthorized')
        return api
    
    def update_api(self, user, api_id, data):
        """Update an existing API"""
        # Vérifier que l'API existe et appartient à l'utilisateur
        api = self.get_api_by_id(user, api_id)
        # Mettre à jour name, description, secret_key, public_key si présents
        # Re-chiffrer les clés si nécessaire
        # Sauvegarder et retourner l'objet
        pass

    def delete_api(self, user, api_id):
        """Delete an API"""
        api = self.get_api_by_id(user, api_id)
        self.api_repo.delete(api)
