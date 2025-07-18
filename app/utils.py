
from werkzeug.security import generate_password_hash

def create_admin_user():
    """
    Crée un admin par défaut si inexistant (username: admin, password: admin)
    """
    from .models import User
    from . import db
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', password=generate_password_hash('admin'), is_admin=True)
        db.session.add(admin)
        db.session.commit()