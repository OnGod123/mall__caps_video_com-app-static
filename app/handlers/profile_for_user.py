from app.extensions import db
from app.database.models import Profile


def create_profile_for_user(user):
    profile = Profile(user_id=user.id, image=None, bio="")
    db.session.add(profile)
    db.session.commit()

