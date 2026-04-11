from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from flask.views import MethodView

from utils.decorator import escola_pertence_ao_usuario
from utils.pagination import criar_paginacao
from models.escola import Escola
from repositories.escola_repository import (
    get_escola_by_id, create_escola, edit_escola, delete_escola
)

class EscolaView(MethodView):
    decorators = [login_required, escola_pertence_ao_usuario]

    def get(self, id=None):   
        if id is not None:
            return render_template("escolas/escola_form.html", escola=get_escola_by_id(id, current_user.id))
          
        if request.endpoint == 'escolas.escola_create':
            return render_template("escolas/escola_form.html", escola=None)
        
        pagination, usuario_admin = criar_paginacao(request, Escola, current_user, "criado_em", True) 
        return render_template("escolas/escolas_list.html", 
                             escolas=pagination.items,
                               pagination=pagination,
                               is_admin=usuario_admin)         
      
    def post(self, id=None):        
        nome_escola = request.form.get('nome')
        cidade_escola = request.form.get('cidade')          

        if request.endpoint == 'escolas.escola_excluir':
            sucesso, erro = delete_escola(id)
            if sucesso:
                flash('Escola excluída com sucesso!', 'success')
            else:
                flash(f'Não foi possível excluir a escolas {erro}', 'error')  

            return redirect(url_for('escolas.escolas_view'))     

        if id is None:
            sucesso, erro = create_escola(nome_escola, cidade_escola, current_user.id)
            mensagem_sucesso = 'Escola criada com sucesso!'
        else:
            sucesso, erro = edit_escola(id, nome_escola, cidade_escola)            
            mensagem_sucesso = 'Escola atualizada com sucesso!'

        if sucesso:
            flash(mensagem_sucesso, 'success')
            return redirect(url_for('escolas.escolas_view'))
        
        flash(f'Erro: {erro}', 'error')
        escola = {'id':id, 'nome': nome_escola, 'cidade': cidade_escola}
        return render_template('escolas/escola_form.html', escola=escola)      