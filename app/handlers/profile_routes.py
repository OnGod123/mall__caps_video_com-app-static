from flask import Blueprint, render_template, request, jsonify
from app.databas.models import Profile, creatuser  # Assuming User model exists
from login_routes import token_required
from yourapp import db

profile_bp = Blueprint('profile_bp', __name__)

@profile_bp.route('/profile/<identifier>', methods=['GET'])
@token_required
def profile(current_user, identifier):
    # Determine if identifier is numeric (user_id) or a string (username)
    if identifier.isdigit():
        user_id = int(identifier)
        user = User.query.get(user_id)
    else:
        user = User.query.filter_by(username=identifier).first()

    if not user or current_user.id != user.id:
        return jsonify({'message': 'Unauthorized access'}), 403

    profile = Profile.query.filter_by(user_id=user.id).first()
    if not profile:
        return jsonify({'message': 'Profile not found'}), 404

    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        return jsonify({
            'name': user.name,
            'image': profile.image,
            'bio': profile.bio,
            'favorite_genres': profile.favorite_genres
        })
    else:
        return render_template("profile.html", user=user, profile=profile)

