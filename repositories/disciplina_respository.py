from extensions import db
from models.disciplina import Disciplina


def get_disciplina_by_id(id, usuario_id):
    disciplina =  db.session.get(Disciplina, id)

    if not disciplina:
        return None
    
    if usuario_id and disciplina.usuario_id != usuario_id:
        return None
    
    return disciplina

def create_disciplina(nome, usuario_id):
    try:
        nova_disciplina = Disciplina(
            nome=nome,
            usuario_id=usuario_id
        )
        db.session.add(nova_disciplina)
        db.session.commit()

        return True, None
    except Exception as e:
        db.session.rollback()
        return False, str(e)
    
def edit_disciplina(id, nome):
    try:
        disciplina = db.session.get(Disciplina, id)

        if not disciplina:
            return False, 'Disciplina não encontrada.'
        
        disciplina.nome = nome

        db.session.commit()

        return True, None
    except Exception as e:
        db.session.rollback()
        return False, str(e)
    
def delete_disciplina(id):
    try:
        disciplina = db.session.get(Disciplina, id)

        if not disciplina:
            return False, 'Disciplina não encontrada.'


        db.session.delete(disciplina)
        db.session.commit()

        return True, None
    except Exception as e:
        db.session.rollback()
        return False, str(e)
