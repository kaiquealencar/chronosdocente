import os
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_login import login_user, login_required, logout_user, current_user
from flask.views import MethodView
from sqlalchemy import select, desc
from dotenv import load_dotenv

from extensions import db, login_manager, migrate
from config import Config
from models.usuario import Usuario
from models.escola import Escola
from models.disciplina import Disciplina
from utils.decorator import escola_pertence_ao_usuario
from utils.helpers import is_admin
from utils.pagination import criar_paginacao
from repositories.escola_repository import get_escola_by_id, create_escola, edit_escola, delete_escola
load_dotenv()

class EscolaView(MethodView):
    decorators = [login_required, escola_pertence_ao_usuario]

    def get(self, id=None):   
        if id is not None:
            return render_template("escolas/escola_form.html", escola=get_escola_by_id(id, current_user.id))
          
        if request.endpoint == 'escola_create':
            return render_template("escolas/escola_form.html", escola=None)
        
        pagination, usuario_admin = criar_paginacao(request, Escola, current_user, "criado_em", True) 
        return render_template("escolas/escolas_list.html", 
                             escolas=pagination.items,
                               pagination=pagination,
                               is_admin=usuario_admin)         
      
    def post(self, id=None):        
        nome_escola = request.form.get('nome')
        cidade_escola = request.form.get('cidade')          

        if request.endpoint == 'escola_excluir':
            sucesso, erro = delete_escola(id)
            if sucesso:
                flash('Escola excluída com sucesso!', 'success')
            else:
                flash(f'Não foi possível excluir a escolas {erro}', 'error')  

            return redirect(url_for('escolas_view'))     

        if id is None:
            sucesso, erro = create_escola(nome_escola, cidade_escola, current_user.id)
            mensagem_sucesso = 'Escola criada com sucesso!'
        else:
            sucesso, erro = edit_escola(id, nome_escola, cidade_escola)            
            mensagem_sucesso = 'Escola atualizada com sucesso!'

        if sucesso:
            flash(mensagem_sucesso, 'success')
            return redirect(url_for('escolas_view'))
        
        flash(f'Erro: {erro}', 'error')
        escola = {'id':id, 'nome': nome_escola, 'cidade': cidade_escola}
        return render_template('escolas/escola_form.html', escola=escola)      


class DisciplinaView(MethodView):    
    def get(self, id=None):
        if id or request.endpoint == 'disciplina_create':
            disciplina_atual = None
            if id:
                disciplina_atual = db.session.get(Disciplina, id)
                if not disciplina_atual:
                    flash('Disciplina não encontrada.', 'error')
                    return redirect(url_for('disciplina_view'))

            return render_template('disciplinas/disciplina_form.html', disciplina=disciplina_atual)
        
        pagination, usuario_admin = criar_paginacao(request, Disciplina, current_user, 'id', True)     

        return render_template('disciplinas/disciplinas_list.html',
                               disciplinas=pagination.items, 
                               pagination=pagination,
                               is_admin=usuario_admin)

            


    def post(self, id=None):
        if request.endpoint == 'disciplina_excluir':
            try:
                disciplina = db.session.get(Disciplina, id)
                if disciplina:
                    db.session.delete(disciplina)
                    db.session.commit()
                    flash('Disciplina removida com sucesso!', 'success')
                else:
                    flash('Disciplina não encontrada.', 'error')
                return redirect(url_for('disciplina_view'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao excluir: {e}', 'error')
                return redirect(url_for('disciplina_view'))
      
        try:
            nome_disciplina = request.form.get('nome')
            
            if id:
                disciplina = db.session.get(Disciplina, id)
                if not disciplina:
                    flash('Disciplina não encontrada para edição', 'error')
                    return redirect(url_for('disciplina_view'))
                
                disciplina.nome = nome_disciplina
                mensagem = "Disciplina Atualizada com sucesso!"
            else:
                nova_disciplina = Disciplina(
                    nome=nome_disciplina,
                    usuario_id=current_user.id
                )
                db.session.add(nova_disciplina)
                mensagem = "Disciplina cadastrada com sucesso!"

            db.session.commit()
            flash(f'{mensagem}', 'success')
            return redirect(url_for('disciplina_view'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao salvar: {e}', 'error')   

            disciplina_atual = db.session.get(Disciplina, id) if id else None 
            return render_template('disciplinas/disciplina_form.html', disciplina=disciplina_atual)
   
def create_app():    
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    migrate.init_app(app, db)

    #Routes Escolas
    app.add_url_rule('/escolas', 
                     view_func=EscolaView.as_view('escolas_view'), 
                     methods=['GET', 'POST'])
    

    app.add_url_rule('/escolas/novo', 
                     view_func=EscolaView.as_view('escola_create'), 
                     methods=['GET', 'POST'])
    
    app.add_url_rule('/escolas/edit/<int:id>', 
                     view_func=EscolaView.as_view('escola_edit'), 
                     methods=['GET', 'POST'])
    
    app.add_url_rule('/escolas/excluir/<int:id>', 
                     view_func=EscolaView.as_view('escola_excluir'), 
                     methods=['GET', 'POST', 'DELETE'])


    #Routes Disciplinas
    app.add_url_rule('/disciplinas', 
                     view_func=DisciplinaView.as_view('disciplina_view'),
                     methods=['GET', 'POST']
                     )
    
    app.add_url_rule('/disciplina/novo',
                     view_func=DisciplinaView.as_view('disciplina_create'),
                     methods=['GET', 'POST'])
    
    app.add_url_rule('/disciplina/edit/<int:id>',
                     view_func=DisciplinaView.as_view('disciplina_edit'),
                     methods=['GET', 'POST'])
    
    app.add_url_rule('/disciplina/delete/<int:id>',
                     view_func=DisciplinaView.as_view('disciplina_excluir'),
                     methods=['GET', 'POST'])
                     

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(Usuario, int(user_id))


    from models.usuario import Usuario
    from models.aula import Aula
    from models.serie import Serie

    return app



app = create_app()

@app.route('/')
@login_required
def index():
    return render_template('index.html', is_admin=is_admin())

@app.route('/usuario/novo', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        username = request.form['username']
        password_plain = request.form['password']
        name = request.form["name"]

        query = select(Usuario).filter_by(username=username)
        verifica_usuario = db.session.execute(query).scalar_one_or_none()

        if  verifica_usuario is not None:
            flash('Este usuário já existe.')
            return redirect(url_for("create_user"))
        
        user = Usuario(username=username)
        user.set_password(password_plain)
        user.name = name

        db.session.add(user)
        db.session.commit()

        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form["name"]


        query = select(Usuario).filter_by(username=username)
        verifica_usuario = db.session.execute(query).scalar_one_or_none()

        if verifica_usuario is not None:
            flash('Este usuário já existe.', 'error')
            return redirect(url_for('register'))
            
        user = Usuario(username=username)
        user.set_password(password)
        user.name =name

        db.session.add(user)
        db.session.commit()
        
        flash('Cadastro realizado com sucesso! Faça login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Usuario.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
            
        flash('Usuário ou senha inválidos.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)