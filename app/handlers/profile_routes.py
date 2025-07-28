from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from yourapp.models import Profile
from login_routes import token_required
from yourapp import db

profile_bp = Blueprint('profile_bp', __name__)

@profile_bp.route('/profile/<int:user_id>', methods=['GET'])
@token_required
def profile(current_user, user_id):
    if current_user.id != user_id:
        return jsonify({'message': 'Unauthorized access'}), 403
    profile = Profile.query.filter_by(user_id=user_id).first()
    if not profile:
        return jsonify({'message': 'Profile not found'}), 404
    return jsonify({
        'name': current_user.name,
        'image': profile.image,
        'bio': profile.bio,
        'favorite_genres': profile.favorite_genres
    })
