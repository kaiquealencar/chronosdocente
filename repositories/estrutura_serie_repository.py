from extensions import db
from models.serie import Serie

def create_serie(nome, ciclo_id, escola_id, usuario_id):
    try:
        nova_serie = Serie(
            nome=nome,
            ciclo_id=ciclo_id,
            escola_id=escola_id,
            usuario_id=usuario_id
        )

        db.session.add(nova_serie)
        db.session.commit()

        return True, None
    except Exception as e:
        db.session.rollback()
        return False, str(e)
    
def edit_serie(id, nome, ciclo_id):
    try:
        serie = db.session.get(Serie, id)

        if not serie:
            return False, "Série não existe."
        
        serie.nome = nome
        serie.ciclo_id = ciclo_id
        db.session.commit()

        return True, None

    except Exception as e:
        db.session.rollback()
        return False, str(e)
def delete_serie(id):
    try:
        serie = db.session.get(Serie, id)

        if not serie:
            return False, "Série não existe."
        
        if serie.tem_vinculos():
            return False, 'Não é possível excluir série com aulas vinculadas.'
        
        db.session.delete(serie)
        db.session.commit()

        return True, None

    except Exception as e:
        db.session.rollback()
        return False, str(e)

