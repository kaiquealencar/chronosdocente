from extensions import db
from sqlalchemy.orm import validates
from sqlalchemy import UniqueConstraint

class Disciplina(db.Model):
    __tablename__ = "disciplinas"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)

    aulas = db.relationship("Aula", back_populates="disciplina")
    usuario = db.relationship("Usuario", back_populates="disciplinas")

    __table_args__ = (
        UniqueConstraint('nome', 'usuario_id', name='uq_disciplina_nome_usuario'),
        db.Index('idx_disciplina_usuario', 'usuario_id'),
    )

    @validates("nome")
    def validate_nome(self, key, nome):
        if not nome:
            raise AssertionError("O nome não pode ficar vazio.")
        
        return nome
    