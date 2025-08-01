from flask import Blueprint, render_template, request, redirect, url_for
from app.database.models import Profile, CreateUser
from app.extensions import db
from app.handlers.login_routes import token_required

profile_bp = Blueprint('profile_bp', __name__)

@profile_bp.route('/profile/update', methods=['GET', 'POST'])
@token_required
def update_profile(current_user):
    profile = Profile.query.filter_by(user_id=current_user.id).first()
    if not profile:
        return "Profile not found", 404

    if request.method == 'POST':
        image = request.form.get('image')
        bio = request.form.get('bio')
        favorite_genres = request.form.get('favorite_genres')

        profile.image = image or profile.image
        profile.bio = bio or profile.bio
        profile.favorite_genres = favorite_genres or profile.favorite_genres

        db.session.commit()

        return redirect(url_for('profile_bp.update_profile'))

    return render_template('update_profile.html', profile=profile, user=current_user)
