from extensions import db
from models.aula import Aula


def create_aula(dia_aula, hora_inicio, hora_fim, disciplina_id, usuario_id,
                escola_id, serie_id):    
    try:    
        nova_aula = Aula(
            dia_aula =  dia_aula,
            hora_inicio = hora_inicio,
            hora_fim = hora_fim,
            disciplina_id = disciplina_id,
            usuario_id = usuario_id,
            escola_id = escola_id,
            serie_id = serie_id            
        )

        db.session.add(nova_aula)
        db.session.commit()

        return True, None
    except Exception as e:
        db.session.rollback()
        return False, str(e)




def edit_aula(id, dia_aula, hora_inicio, hora_fim, disciplina_id, usuario_id,
                escola_id, serie_id):    
    try:    
        aula = db.session.get(Aula, id)

        if not aula:
            return False, "Aula não encontrada"
        
        aula.dia_aula = dia_aula
        aula.hora_inicio = hora_inicio
        aula.hora_fim = hora_fim
        aula.disciplina_id = disciplina_id
        aula.usuario_id = usuario_id
        aula.escola_id = escola_id
        aula.serie_id = serie_id
        
        db.session.commit()

        return True, None
    except Exception as e:
        db.session.rollback()
        return False, str(e)



def delete_aula(id):
    try:    
        aula = db.session.get(Aula, id)

        if not aula:
            return False, "Aula não encontrada"
        
        db.session.delete(aula)
        db.session.commit()

        return True, None
    except Exception as e:
        db.session.rollback()
        return False, str(e)

