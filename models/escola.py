from datetime import datetime, timezone
from sqlalchemy.orm import validates
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import  relationship
from sqlalchemy import func
from extensions import db


class Escola(db.Model):
    __tablename__ = "escolas"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    cidade = db.Column(db.String(150), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    criado_em = db.Column(db.DateTime, 
                      default=lambda: datetime.now(timezone.utc),  
                      server_default=func.now(),                   
                      nullable=False)

    aulas = relationship("Aula", back_populates="escola")
    usuario = relationship("Usuario", back_populates="escolas")
    ciclos = db.relationship("Ciclo", back_populates="escola", cascade="all, delete-orphan")
    series = relationship("Serie", back_populates="escola")

    __table_args__ = (
        UniqueConstraint('nome', 'usuario_id', name='uq_escola_nome_usuario'),
        
        db.Index('idx_escola_usuario', 'usuario_id'),
        
        db.Index('idx_escola_cidade', 'cidade'),
    )

    @validates("nome")
    def validate_nome(self, key, nome):
        if not nome:
            raise AssertionError("O nome não pode ficar vazio.")
        
        return nome
    

