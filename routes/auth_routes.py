"""
Kisan Web Project - Authentication & Farmer Directory Routes
Handles multi-role user registration, login with JWT & sessions, profile retrieval, and public farmer directory.
"""
from flask import Blueprint, request, jsonify, session
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from extensions import db
from models import User

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user (Farmer, Buyer, Admin)."""
    data = request.get_json() or {}
    name = data.get('name', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '').strip()
    role = data.get('role', 'farmer').lower()
    phone = data.get('phone', '').strip()
    state = data.get('state', '').strip()
    district = data.get('district', '').strip()
    farm_size_acres = float(data.get('farm_size_acres', 0) or 0)
    primary_crops = data.get('primary_crops', '')

    if not name or not email or not password:
        return jsonify({'error': 'Name, email, and password are required fields.'}), 400

    if role not in ['farmer', 'buyer', 'admin']:
        role = 'farmer'

    # Check if user already exists
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'An account with this email already exists.'}), 409

    # Create user
    user = User(
        name=name,
        email=email,
        role=role,
        phone=phone,
        state=state,
        district=district,
        farm_size_acres=farm_size_acres,
        primary_crops=primary_crops,
        is_verified=(role == 'farmer')  # Demo auto-verification for farmers
    )
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    # Generate JWT token
    token = create_access_token(identity=str(user.id))
    session['user_id'] = user.id
    session['user_role'] = user.role

    return jsonify({
        'message': f'Welcome to Kisan, {user.name}!',
        'access_token': token,
        'user': user.to_dict()
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    """Authenticate user with email and password."""
    data = request.get_json() or {}
    email = data.get('email', '').strip().lower()
    password = data.get('password', '').strip()

    if not email or not password:
        return jsonify({'error': 'Email and password are required.'}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid credentials provided.'}), 401

    token = create_access_token(identity=str(user.id))
    session['user_id'] = user.id
    session['user_role'] = user.role

    return jsonify({
        'message': f'Welcome back, {user.name}!',
        'access_token': token,
        'user': user.to_dict()
    }), 200


@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    """Retrieve logged-in user profile from session or bearer token."""
    user_id = session.get('user_id')
    
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        # We can extract or use get_jwt_identity if decorated
        pass

    if not user_id:
        # Fallback to guest or return 401
        return jsonify({'authenticated': False, 'user': None}), 200

    user = User.query.get(user_id)
    if not user:
        session.clear()
        return jsonify({'authenticated': False, 'user': None}), 200

    return jsonify({
        'authenticated': True,
        'user': user.to_dict()
    }), 200


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Log out current user."""
    session.clear()
    return jsonify({'message': 'Logged out successfully.'}), 200


@auth_bp.route('/farmers', methods=['GET'])
def get_farmers_directory():
    """Public directory listing registered and verified local farmers."""
    state_filter = request.args.get('state', '').strip()
    crop_filter = request.args.get('crop', '').strip()

    query = User.query.filter_by(role='farmer')
    if state_filter:
        query = query.filter(User.state.ilike(f'%{state_filter}%'))
    if crop_filter:
        query = query.filter(User.primary_crops.ilike(f'%{crop_filter}%'))

    farmers = query.order_by(User.is_verified.desc(), User.id.desc()).limit(50).all()
    return jsonify({
        'count': len(farmers),
        'farmers': [f.to_dict() for f in farmers]
    }), 200
