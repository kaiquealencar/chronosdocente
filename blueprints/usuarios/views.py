from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from flask.views import MethodView

from utils.pagination import criar_paginacao
from utils.decorator import admin_required
from models.usuario import Usuario
from repositories.usuario_repository import (get_usuarios, create_usuario, edit_usuario, delete_usuario)

class UsuarioView(MethodView):
    decorators = [admin_required, login_required]

    def get(self, id=None):

        if id is not None:         
            edit_usuario = Usuario.query.get_or_404(id)
            return render_template('usuarios/usuario_form.html', usuario=edit_usuario)
        
        if request.endpoint == 'usuarios.usuario_create':
            return render_template('usuarios/usuario_form.html', usuario = None)
        

        pagination, usuario_admin = criar_paginacao(request, Usuario, current_user, 'id', True)

        return render_template('usuarios/usuarios_list.html',
                               usuarios=pagination.items,
                               pagination=pagination,
                               is_admin = usuario_admin)
    

    def post(self, id=None):

        username = request.form.get('username')
        password = request.form.get('password')
        name = request.form.get('username')
        tipo_usuario = 'admin' if 'is_admin' in request.form else 'professor'   
        
        is_admin= 'is_admin' in request.form
        ativo = 'ativo' in request.form

        if request.endpoint == 'usuarios.usuario_delete':
            usuario_para_excluir = Usuario.query.get_or_404(id)

            if usuario_para_excluir.tem_vinculos():
                flash('Não é possível exlcuir um usário que possui dados vinculados no sistema.', 'error')
                return redirect(url_for('usuarios.usuario_view'))        
        
            success, erro = delete_usuario(id, current_user.id)

            if success:
                flash('Usuário excluído com sucesso!', 'success')
            else:
                flash('Não foi possível excluir o usuários.', 'error')
            
            return redirect(url_for('usuarios.usuario_view'))
        
        if id is None:
            successo, error = create_usuario(
                username, 
                password,
                name,                
                is_admin,
                ativo
            )
            mensagem_sucesso = 'Usuário cadastrado com sucesso!'
        else:
            successo, error = edit_usuario(
                id,
                username,
                name,                
                is_admin,
                ativo,
                password
            )

            mensagem_sucesso = 'Usuário editado com sucesso!'

            if successo:
                flash(mensagem_sucesso, 'success')
                return redirect(url_for('usuarios.usuario_view'))
            
            flash(f'Erro: {erro}', 'error')
            usuario_atual = {'id': id, 'name': name}

            return render_template('usuarios/usuario_form.html', usuario=usuario_atual)
        