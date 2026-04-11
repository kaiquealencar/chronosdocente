from extensions import db
from models.escola import Escola


def get_escola_by_id(escola_id, usuario_id):
    escola =  db.session.get(Escola, escola_id)    
    if not escola:
        return None
    
    if usuario_id and escola.usuario_id != usuario_id:
        return None
    
    return escola

def create_escola(nome_escola, cidade_escola, usuario_id):
    try:
        nova_escola = Escola(
            nome=nome_escola,
            cidade=cidade_escola,
            usuario_id=usuario_id
        )
        db.session.add(nova_escola)
        db.session.commit()

        return True, None    
    except Exception as e:
        db.session.rollback()
        return False, str(e)    

def edit_escola(id, nome, cidade): 
    try:
        escola = db.session.get(Escola, id)
        escola.nome = nome    
        escola.cidade = cidade

        db.session.commit()
        return True, None
    except Exception as e:
        db.session.rollback()
        return False, str(e) 


def delete_escola(escola_id):
    try:
        escola = db.session.get(Escola, escola_id)
        if escola:
            db.session.delete(escola)
            db.session.commit()     

            return True, None   
    except Exception as e:
        db.session.rollback()    
        return False, str(e)