from extensions import db
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship

class Serie(db.Model):
    __tablename__ = "series"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False) 
    
    escola_id = db.Column(db.Integer, db.ForeignKey("escolas.id"), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)

    aulas = db.relationship("Aula", back_populates="serie")
    escola = relationship("Escola", back_populates="series")
    usuario = relationship("Usuario", back_populates="series")
    
    __table_args__ = (
        UniqueConstraint('nome', 'escola_id', 'usuario_id', name='_serie_escola_uc'),
    )