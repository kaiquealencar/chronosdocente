from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user
from repositories.escola_repository import get_escola_by_id
from repositories.disciplina_respository import get_disciplina_by_id

def escola_pertence_ao_usuario(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            escola = get_escola_by_id(id, usuario_id=current_user.id)

            if not escola:
                flash('Acesso negado.', 'error')
                return redirect(url_for('escolas_view'))
            
        return func(*args, **kwargs)
    
    return wrapper

def disciplina_pertence_ao_usuario(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            disciplina = get_disciplina_by_id(id, usuario_id=current_user.id)

            if not disciplina:
                flash('Acesso negado.', 'error')
                return redirect(url_for('disciplina_view'))
            
        return func(*args, **kwargs)
    
    return wrapper



def admin_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not getattr(current_user, 'is_admin', False):
            flash('Acesso restrito a administradores.', 'error')
            return redirect(url_for('index'))
        return func(*args, **kwargs)
    return decorated_function


    
