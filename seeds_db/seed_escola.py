import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from extensions import db
from models.escola import Escola
from models.usuario import Usuario
from sqlalchemy import select

app = create_app()

def popular_banco():
    with app.app_context():
        username_teste = 'kaique_admin' 
        user = db.session.execute(select(Usuario).filter_by(username=username_teste)).scalar_one_or_none()

        if not user:
            print(f"Erro: Usuário '{username_teste}' não encontrado. Crie o usuário primeiro.")
            return

        print(f"Cadastrando escolas para o usuário: {user.username}")

        cidades = ["São Paulo", "Rio de Janeiro", "Curitiba", "Belo Horizonte", "Salvador"]
        
        for i in range(1, 31):
            nova_escola = Escola(
                nome=f"Escola Municipal {i:02d}",
                cidade=cidades[i % len(cidades)],
                usuario_id=user.id
            )
            db.session.add(nova_escola)

        try:
            db.session.commit()
            print("✅ Sucesso: 30 escolas cadastradas para teste de paginação!")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Erro ao popular banco: {e}")

if __name__ == "__main__":
    popular_banco()