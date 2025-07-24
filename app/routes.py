from flask import Blueprint, request, jsonify
from app.services import (
    get_all_users,
    get_user_by_id,
    create_user,
    update_user,
    delete_user,
    search_users_by_full_name,
    login_user
)

bp = Blueprint('routes', __name__)

@bp.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'User API is running'}), 200


@bp.route('/users', methods=['GET'])
def list_users():
    users = get_all_users()
    return jsonify(users), 200


@bp.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = get_user_by_id(user_id)
    if user:
        return jsonify(user), 200
    else:
        return jsonify({'error': 'User not found'}), 404


@bp.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()

    required_fields = ['username', 'email', 'full_name', 'password']
    if not data or not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing username, email, full_name, or password'}), 400

    created = create_user(
        username=data['username'],
        email=data['email'],
        full_name=data['full_name'],
        password=data['password']
    )

    if not created:
        return jsonify({'error': 'User already exists'}), 409

    return jsonify({'message': 'User created'}), 201


@bp.route('/user/<int:user_id>', methods=['PUT'])
def modify_user(user_id):
    data = request.get_json()
    if not data or 'email' not in data or 'full_name' not in data:
        return jsonify({'error': 'Missing email or full_name'}), 400

    updated = update_user(user_id, data)
    if not updated:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({'message': 'User updated'}), 200


@bp.route('/user/<int:user_id>', methods=['DELETE'])
def remove_user(user_id):
    deleted = delete_user(user_id)
    if not deleted:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'message': 'User deleted'}), 200


@bp.route('/search', methods=['GET'])
def search_users():
    name = request.args.get('name')
    if not name:
        return jsonify({'error': 'Missing name parameter'}), 400
    users = search_users_by_full_name(name)
    return jsonify(users), 200


@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Missing email or password'}), 400

    user = login_user(data['email'], data['password'])
    if user:
        return jsonify({'message': 'Login successful', 'user': user}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401