import os
from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import select
from flask_login import login_user, login_required, logout_user, current_user
from dotenv import load_dotenv
from extensions import db, login_manager, migrate
from config import config

from models.usuario import Usuario
from utils.helpers import is_admin


load_dotenv()


def create_app():    
    app = Flask(__name__)
    env = os.getenv('FLASK_ENV', 'default')
    app.config.from_object(config[env])    

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    migrate.init_app(app, db)

    import models

    from blueprints.disciplinas import disciplinas_bp
    from blueprints.escolas import escolas_bp   
    from blueprints.usuarios import usuarios_bp


    app.register_blueprint(disciplinas_bp)
    app.register_blueprint(escolas_bp)
    app.register_blueprint(usuarios_bp)
   
   

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(Usuario, int(user_id))

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