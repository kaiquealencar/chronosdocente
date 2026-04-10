from extensions import db
from sqlalchemy.orm import validates
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import  relationship


class Escola(db.Model):
    __tablename__ = "escolas"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    cidade = db.Column(db.String(150), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)

    aulas = relationship("Aula", back_populates="escola")
    usuario = relationship("Usuario", back_populates="escolas")
    series = relationship("Serie", back_populates="escola")

    __table_args__ = (
        UniqueConstraint('nome', 'usuario_id', name='uq_escola_nome_usuario'),
    )

    @validates("nome")
    def validate_nome(self, key, nome):
        if not nome:
            raise AssertionError("O nome não pode ficar vazio.")
        
        return nome
    

