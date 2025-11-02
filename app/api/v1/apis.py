from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.api import API
from app.models.user import User
from app.utils.crypto import encrypt, decrypt, generate_key


api = Namespace('apis', description='APIs operations')

user_model = api.model('SecretUser', {
    'id': fields.String(description='User ID'),
    'username': fields.String(description='Username of the user'),
    'email': fields.String(description='Email of the user'),
})

api_model = api.model('APIs', {
    'id': fields.String(description='Secret ID'),
    'name': fields.String(required=True, description='API name'),
    'description': fields.String(description='API description'),
    'public_key': fields.String(description='Public key (optional)'),
    'secret_key': fields.String(description='Secret key (optional)'),
    'user': fields.Nested(user_model, description='User of the API')

})

@api.route('/')
class APIList(Resource):
    @api.expect(api_model)
    @api.response(201, 'API succesfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        "Register a new API"
        current_user_id = get_jwt_identity()
        data = request.get_json()

        if not data.get('secret_key') and not data.get('public_key'):
            return {'error': 'At least one key must be provided'}, 400
        
        user = User.query.get(current_user_id)
        if not user:
            return {'error': 'User not found'}, 404
        
        api = API(
            name = data['name'],
            description = data.get('description', ''),
            user = user
        )

        user_key = user.get_encryption_key()
        
        if data.get('secret_key'):
            api.set_secret_key(data['secret_key'], user_key)
        if data.get('public_key'):
            api.set_public_key(data['public_key'], user_key)
        
        api.save()

        return api.to_dict(), 201
