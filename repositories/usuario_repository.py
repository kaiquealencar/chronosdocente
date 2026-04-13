from extensions import db
from models.usuario import Usuario
from utils.helpers import is_admin

def get_usuarios():
    if not is_admin():
        return None
        
    return Usuario.query.filter_by(ativo=True).all()

def create_usuario(username, password, name, tipo_usuario, is_admin, ativo):
    try:
        novo_usuario = Usuario(
            username=username,
            name=name,
            tipo_usuario=tipo_usuario,
            is_admin=is_admin,
            ativo=ativo      
        )


        novo_usuario.set_password(password)

        db.session.add(novo_usuario)
        db.session.commit()

        return True, None
    except Exception as e:
        db.session.rollback()
        return False, str(e)
    

def edit_usuario(id, username, name, tipo_usuario, is_admin, ativo, password=None):
    try:
        usuario = db.session.get(Usuario, id)

        if not usuario:
            return False, "Usuário não encontrado."
        
        usuario.username = username
        usuario.name = name
        usuario.tipo_usuario = tipo_usuario
        usuario.is_admin = is_admin
        usuario.ativo = ativo
        
        if password: 
            usuario.set_password(password)

        
        db.session.commit()
        return True, None    

    except Exception as e:
        db.session.rollback()
        return False, str(e)


def delete_usuario(id, current_id):
    try:
        usuario = db.session.get(Usuario, id)

        if not usuario:
            return False, "Usuário não encontrado."  

        if usuario.id == current_id:
             return False, "Você não pode excluir sua própria conta."   

        db.session.delete(usuario)
        db.session.commit()
        return True, None    

    except Exception as e:
        db.session.rollback()
        print(f"Erro ao deletar usuário: {e}")
        return False, str(e)
