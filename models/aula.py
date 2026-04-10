from extensions import db
from sqlalchemy.orm import  relationship

class Aula(db.Model):
    __tablename__ = "aulas"
    id = db.Column(db.Integer, primary_key=True)
    dia_aula = db.Column(db.DateTime, nullable=False)
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fim = db.Column(db.Time, nullable=False)
    
    disciplina_id = db.Column(db.Integer, db.ForeignKey("disciplinas.id"), nullable=False) 
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    escola_id = db.Column(db.Integer, db.ForeignKey("escolas.id"), nullable=False)
    serie_id = db.Column(db.Integer, db.ForeignKey("series.id"), nullable=False)

    disciplina = relationship("Disciplina", back_populates="aulas")
    professor = relationship("Usuario", back_populates="aulas")
    escola = relationship("Escola", back_populates="aulas")
    serie = db.relationship("Serie", back_populates="aulas")

    criado_em = db.Column(db.DateTime, default=db.func.now())
