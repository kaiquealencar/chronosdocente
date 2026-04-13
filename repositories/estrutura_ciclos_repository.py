from extensions import db
from models.serie import Ciclo

def create_ciclos(nome, escola_id, usuario_id, ordem=1):
    try:
        novo_ciclo = Ciclo(
            nome=nome,
            escola_id=escola_id,
            usuario_id=usuario_id,
            ordem=ordem
        )

        db.session.add(novo_ciclo)
        db.session.commit()

        return True, None
    except Exception as e:
        db.session.rollback()
        return False, str(e)

def edit_ciclos(id, nome, ordem=1):
    try:
        ciclo = db.session.get(Ciclo, id)

        if not ciclo:
            return False, "Ciclo não encontrado."
        
        ciclo.nome = nome,
        ciclo.ordem = ordem

        db.session.commit()

        return True, None
    except Exception as e:
        db.session.rollback()
        return False, str(e)
    
def delete_ciclo(id):
    try:
        ciclo = db.session.get(Ciclo, id)

        if not ciclo:
            return False, "Ciclo não encontrado!"
        
        db.session.delete(ciclo)
        db.session.commit()

        return True, None
    except Exception as e:
        db.session.rollback()
        return False, str(e)
