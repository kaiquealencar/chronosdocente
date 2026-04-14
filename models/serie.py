from extensions import db
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates

class Ciclo(db.Model):
    __tablename__ = "ciclos"
    id = db.Column(db.Integer, primary_key=True) 
    nome = db.Column(db.String(200), nullable=False)
    escola_id = db.Column(db.Integer, db.ForeignKey("escolas.id"), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    ordem = db.Column(db.Integer, default=1)

    series = db.relationship("Serie", back_populates="ciclo", cascade="all, delete-orphan")
    escola = db.relationship("Escola", back_populates="ciclos") 
    usuario = db.relationship("Usuario", back_populates="ciclos")

    __table_args__ = (
        UniqueConstraint('nome', 'escola_id', 'usuario_id', name='_ciclo_escola_uc'),
        db.Index('idx_ciclo_escola', 'escola_id'), 
    )

    def tem_vinculos(self):
        return len(self.series) > 0

    @validates("nome")
    def validate_nome(self, key, nome):
        if not nome or not nome.strip():
            raise ValueError("O nome do ciclo não pode estar vazio.")
        
        nome_limpo = " ".join(nome.split())

        if len(nome_limpo) < 3:
            raise ValueError("Escreva o nome completo do ciclo.")
        
        return nome_limpo
    
    @validates("ordem")
    def validate_ordem(self, key, ordem):
        if ordem is not None and ordem < 1:
            raise ValueError("A ordem deve ser um número positivo.")
        return ordem
    

class Serie(db.Model):
    __tablename__ = "series"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False) 
    ciclo_id = db.Column(db.Integer, db.ForeignKey("ciclos.id"), nullable=False)
    escola_id = db.Column(db.Integer, db.ForeignKey("escolas.id"), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)

    ciclo = db.relationship("Ciclo", back_populates="series")
    escola = db.relationship("Escola", back_populates="series")
    usuario = db.relationship("Usuario", back_populates="series")
    aulas = db.relationship("Aula", back_populates="serie")
    
    __table_args__ = (
        db.UniqueConstraint('nome', 'ciclo_id', 'escola_id', name='_nome_ciclo_escola_uc'),
        
        db.Index('idx_serie_escola', 'escola_id'),
        db.Index('idx_serie_ciclo', 'ciclo_id'),
    )   

    def tem_vinculos(self):
        return len(self.aulas) > 0

    @validates("nome")
    def validate_nome(self, key, nome):
        if not nome or not nome.strip():
            raise ValueError("O nome da série não pode estar vazio.")
        
        return nome.strip()