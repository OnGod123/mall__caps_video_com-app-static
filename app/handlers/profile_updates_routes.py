import os
from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from app.database.models import Profile
from app.extensions import db
from app.handlers.login_routes import token_required
from app.extensions import csrf

profile_bp = Blueprint('profile_bp', __name__)

UPLOAD_FOLDER = os.path.join('static', 'uploads')

@profile_bp.route('/profile/update', methods=['GET', 'POST'])
@token_required
@csrf.exempt
def update_profile(current_user):
    print("[DEBUG] Entered update_profile route")

    profile = Profile.query.filter_by(user_id=current_user.id).first()
    if not profile:
        print("[ERROR] Profile not found for user_id:", current_user.id)
        return "Profile not found", 404

    if request.method == 'POST':
        try:
            print("[DEBUG] Received POST request")
            print("[DEBUG] request.form:", request.form)
            print("[DEBUG] request.files:", request.files)

            # Ensure upload folder exists
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)

            # Handle file upload
            image_file = request.files.get('image')
            if image_file and image_file.filename != '':
                filename = secure_filename(image_file.filename)  # Remove spaces & unsafe chars
                upload_path = os.path.join(UPLOAD_FOLDER, filename)
                image_file.save(upload_path)
                profile.image = f"/static/uploads/{filename}"
                print("[DEBUG] Saved image as:", profile.image)
            else:
                print("[DEBUG] No new image uploaded")

            # Handle text fields
            bio = request.form.get('bio')
            favorite_genres = request.form.get('favorite_genres')
            print("[DEBUG] Bio:", bio)
            print("[DEBUG] Favorite Genres:", favorite_genres)

            profile.bio = bio or profile.bio
            profile.favorite_genres = favorite_genres or profile.favorite_genres

            db.session.commit()
            print("[DEBUG] Profile updated successfully")

            return redirect(url_for('profile_view_bp.profile', identifier=current_user.username))

        except Exception as e:
            print("[ERROR] Exception while updating profile:", e, flush=True)
            return f"Error: {str(e)}", 500

    print("[DEBUG] Rendering update_profile.html")
    return render_template('update_profile.html', profile=profile, user=current_user)

