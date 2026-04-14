from flask_login import current_user

def is_admin():
    return current_user.is_authenticated and getattr(current_user, 'is_admin', False)