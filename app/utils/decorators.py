from functools import wraps
from flask import redirect, url_for
from flask_login import current_user

def role_required(required_role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('login'))  # Redirigir si no está autenticado
            if not current_user.is_validated:
                return redirect(url_for('unauthorized'))  # Redirigir si no está validado
            if current_user.role != required_role:
                return redirect(url_for('unauthorized'))  # Redirigir si el rol no es el esperado
            return func(*args, **kwargs)
        return wrapper
    return decorator



def roles_required(roles):
    def decorated_function(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if set(roles).issubset({r.name for r in current_user.roles}):
                return f(*args, **kwargs)
            else:
                # return get_business_requirement_error_response(
                #     PermissionsDeniedError, 403
                # )
                return redirect(url_for('unauthorized'))

        return wrapper

    return decorated_function