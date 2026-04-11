from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from extensions import db

class Usuario(db.Model, UserMixin):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(150))
    tipo_usuario = db.Column(db.String(20), default="professor")
    is_admin = db.Column(db.Boolean, default=False)

    aulas = relationship("Aula", back_populates="professor")
    disciplinas = relationship("Disciplina", back_populates="usuario")
    escolas = relationship("Escola", back_populates="usuario") 
    series = relationship("Serie", back_populates="usuario")

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


    @property
    def first_name(self):
        if self.name:
            return self.name.split()[0]
        
        return self.username
    
