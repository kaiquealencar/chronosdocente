from extensions import db
from sqlalchemy.orm import validates

class Disciplina(db.Model):
    __tablename__ = "disciplinas"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), unique=True, nullable=False)

    aulas = db.relationship("Aula", back_populates="disciplina")

    @validates("nome")
    def validate_nome(self, key, nome):
        if not nome:
            raise AssertionError("O nome não pode ficar vazio.")
        
        return nome
    