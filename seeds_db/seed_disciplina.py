import sys
import os

# 1. Configuração do PATH (deve vir antes dos imports do projeto)
# Adiciona a pasta pai (raiz do projeto) ao caminho de busca do Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 2. Imports do Projeto
from app import create_app
from extensions import db
from models.usuario import Usuario
from models.disciplina import Disciplina
from sqlalchemy import select

# 3. Inicialização do Contexto
app = create_app()

def seed_disciplinas():
    with app.app_context():
        # 1. Localizar o usuário alvo
        username_alvo = 'kaique_admin'
        print(f"🔍 Buscando usuário: {username_alvo}...")
        
        user = db.session.execute(
            select(Usuario).filter_by(username=username_alvo)
        ).scalar_one_or_none()

        if not user:
            print(f"❌ Erro: Usuário '{username_alvo}' não encontrado.")
            print("Certifique-se de que o usuário existe no banco antes de rodar este seed.")
            return

        # 2. Lista de disciplinas para cadastrar
        materias = [
            "Matemática", "Língua Portuguesa", "História", "Geografia", 
            "Ciências", "Educação Física", "Artes", "Inglês", 
            "Física", "Química", "Biologia", "Filosofia", "Sociologia",
            "Ensino Religioso", "Literatura", "Redação"
        ]

        print(f"🚀 Iniciando cadastro para: {user.username} (ID: {user.id})")

        novas_adicionadas = 0
        pulas = 0

        for nome in materias:
            # 3. Checagem de Duplicidade (evita IntegrityError)
            existente = db.session.execute(
                select(Disciplina).filter_by(nome=nome, usuario_id=user.id)
            ).scalar_one_or_none()

            if not existente:
                nova_disc = Disciplina(
                    nome=nome,
                    usuario_id=user.id
                )
                db.session.add(nova_disc)
                novas_adicionadas += 1
                print(f"  + Adicionando: {nome}")
            else:
                pulas += 1

        # 4. Finalização e Commit
        try:
            db.session.commit()
            print(f"\n--- ✨ Relatório Final ---")
            print(f"✅ Novas disciplinas: {novas_adicionadas}")
            print(f"⚠️ Já existentes (puladas): {pulas}")
            print(f"--------------------------")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Erro crítico ao salvar no banco: {e}")

if __name__ == "__main__":
    seed_disciplinas()