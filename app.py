import os
from flask import Flask, render_template, request, redirect, url_for, flash, current_app
from sqlalchemy import select, or_
from flask_login import login_user, login_required, logout_user, current_user
from dotenv import load_dotenv
from extensions import db, login_manager, migrate, mail
from config import config
from services.email_utils import send_confirmation_email

from models.usuario import Usuario
from utils.helpers import is_admin


load_dotenv()


def create_app():    
    app = Flask(__name__)
    env = os.getenv('FLASK_ENV', 'default')
    app.config.from_object(config[env])    

    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    migrate.init_app(app, db)

    import models

    from blueprints.disciplinas import disciplinas_bp
    from blueprints.escolas import escolas_bp   
    from blueprints.usuarios import usuarios_bp
    from blueprints.estrutura import estrutura_bp
    from blueprints.aulas import aulas_bp


    app.register_blueprint(disciplinas_bp)
    app.register_blueprint(escolas_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(estrutura_bp)
    app.register_blueprint(aulas_bp)
   
   

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
        email = request.form['email']
        name = request.form["name"]


        query = select(Usuario).where(
            or_(Usuario.username == username, Usuario.email == email)
        )       
        
        verifica_usuario = db.session.execute(query).scalar_one_or_none()

        if verifica_usuario is not None:
            if verifica_usuario.email == email:
                flash('Este e-mail já está cadastrado para outro usuário.', 'error')
            else:
                flash('Este usuário já existe.', 'error')

            return redirect(url_for('register'))
            
        user = Usuario(username=username)
        user.set_password(password)
        user.name =name
        user.email = email

        db.session.add(user)
        db.session.commit()
        
        try:
            send_confirmation_email(user.email)
            flash('Um link de confirmação foi enviado!', 'success')
        except Exception as e:
            print(f"Erro ao enviar: {e}") 
            flash('Conta criada, mas houve um erro ao enviar o e-mail de confirmação. Entre em contato com o suporte.', 'warning')
        
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/confirm/<token>')
def confirm_email(token):
    from itsdangerous import URLSafeTimedSerializer
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

    try:
        email = serializer.loads(token, salt='email-confirm', max_age=3600)
    except:
        flash('O link de confirmação é inválido ou expirou', 'error')
        return redirect(url_for('login'))
    
    usuario = Usuario.query.filter_by(email=email).first_or_404()
    usuario.verified = True
    db.session.commit()

    flash('E-mail confirmado com sucesso!', 'success')
    return redirect(url_for('login'))


@app.before_request
def check_user_verification():
    allowed_routes = ['login', 'register', 'confirm_email', 'static', 'logout']

    if request.endpoint in allowed_routes:
        return
    
    if current_user.is_authenticated:
        if not current_user.verified:
            logout_user()
            flash('Por favor, confirme seu e-mail para acessar essa página', 'warning')
            return redirect(url_for('index'))



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Usuario.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            if not user.verified:
                flash('Por favor confirme seu email antes de acessar a plataforma', 'warning')
                return redirect(url_for('login'))
            
            
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
    app.run()