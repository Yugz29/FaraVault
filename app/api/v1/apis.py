from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import FaraVault
from app.models import User


api = Namespace('apis', description='APIs operations')

user_model = api.model('User', {
    'id': fields.String(description='User ID'),
    'username': fields.String(description='Username of the user'),
    'email': fields.String(description='Email of the user'),
})

api_model = api.model('APIs', {
    'id': fields.String(description='API ID'),
    'name': fields.String(required=True, description='API name'),
    'description': fields.String(description='API description'),
    'public_key': fields.String(description='Public key (optional)'),
    'secret_key': fields.String(description='Secret key (optional)'),
    'user': fields.Nested(user_model, description='User of the API')

})

facade = FaraVault()

@api.route('/')
class APIList(Resource):
    @api.expect(api_model)
    @api.response(201, 'API successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new API"""
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        data = request.get_json()
        return facade.create_api(current_user, data)

    @api.response(200, 'List of APIs retrieved successfully')
    @api.response(404, 'User not found')
    @jwt_required()
    def get(self):
        """Retrieve all APIs for the current user"""
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        return facade.get_all_apis(current_user)

@api.route('/<string:api_id>')
class APIResource(Resource):
    @api.response(200, 'API retrieved successfully')
    @api.response(404, 'API not found')
    @jwt_required()
    def get(self, api_id):
        """Retrieve an API by ID"""
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        return facade.get_api_by_id(current_user, api_id)

    @api.response(200, 'API updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'API not found or unauthorized')
    @jwt_required()
    def put(self, api_id):
        """Update an API"""
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        data = request.get_json()

        updated_api = facade.update_api(current_user, api_id, data)
        return updated_api.to_dict(), 200
