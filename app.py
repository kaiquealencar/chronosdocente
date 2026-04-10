import os
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_login import login_user, login_required, logout_user, current_user
from flask.views import MethodView
from sqlalchemy import select, or_
from dotenv import load_dotenv

from extensions import db, login_manager, migrate
from config import Config
from models.usuario import Usuario
from models.escola import Escola

load_dotenv()

def is_admin():
    return current_user.is_authenticated and getattr(current_user, 'is_admin', False)


class EscolaView(MethodView):
    decorators = [login_required]

    def get(self, id=None):
        if id or request.endpoint == 'escola_create':
            escola = db.session.get(Escola, id)
            return render_template("escolas/escola_form.html", escola=escola)
        
        try:
            page = request.args.get('page', 1, type=int)
            if page < 1:
                page = 1
        except (TypeError, ValueError):
            page = 1
            
        stmt = select(Escola)

        if not is_admin():
            stmt = stmt.where(Escola.usuario_id == current_user.id)

        stmt = stmt.order_by(Escola.nome)

        pagination = db.paginate(stmt, page=page, per_page=6, error_out=False)

        return render_template("escolas/escolas_list.html", 
                               escolas=pagination.items,
                               pagination=pagination,
                               is_admin=is_admin())
    
    def post(self, id=None):
        if request.endpoint == 'escola_excluir':
            try:
                escola = db.session.get(Escola, id)
                if escola:
                    db.session.delete(escola)
                    db.session.commit()
                    flash('Escola removida com sucesso!', 'success')
                else:
                    flash('Escola não encontrada.', 'error')

                return redirect(url_for('escolas_view'))

            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao excluir: {e}', 'error')
                return redirect(url_for('escolas_view'))
      
        try:
            nome_escola = request.form.get('nome')
            cidade_escola = request.form.get('cidade')
            
            if id:
                escola = db.session.get(Escola, id)
                if not escola:
                    flash('Escola não encontrada para edição', 'error')
                    return redirect(url_for('escolas_view'))
                
                escola.nome = nome_escola
                escola.cidade = cidade_escola
                mensagem = "Escola Atualizada com sucesso!"
            else:
                nova_escola = Escola(
                    nome=nome_escola,
                    cidade=cidade_escola,
                    usuario_id = current_user.id
                )
                db.session.add(nova_escola)
                mensagem = "Escola cadastrada com sucesso!"

            db.session.commit()
            flash(f'{mensagem}', 'success')
            return redirect(url_for('escolas_view'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Não foi possível cadastrar a escola. Erro: {e}', 'error')   

            escola_atual = db.session.get(Escola, id) if id else None 
            return render_template('escolas/escola_form.html', escola=escola_atual)

    def delete(self, id):
        try:
            escola = db.session.get(Escola, id)

            if not escola:
                return {'messsage': 'Escola não encontrada'}, 400
            
            db.session.delete(escola)
            db.session.commit()

            flash('Escola excluída com sucesso', 'success')
            return {'message': 'Excluído'}, 200

        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 500



def create_app():    
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    migrate.init_app(app, db)

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


    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(Usuario, int(user_id))


    from models.usuario import Usuario
    from models.aula import Aula
    from models.disciplina import Disciplina
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