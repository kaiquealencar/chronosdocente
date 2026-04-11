from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from flask.views import MethodView

from utils.decorator import disciplina_pertence_ao_usuario
from utils.pagination import criar_paginacao
from models.disciplina import Disciplina
from repositories.disciplina_respository import (
    get_disciplina_by_id, create_disciplina, edit_disciplina, delete_disciplina
)

class DisciplinaView(MethodView):    
    decorators = [disciplina_pertence_ao_usuario, login_required]

    def get(self, id=None):
        
        if id is not None:
            return render_template("disciplinas/disciplina_form.html", disciplina=get_disciplina_by_id(id, current_user.id))
        
        if request.endpoint == 'disciplinas.disciplina_create':
            return render_template("disciplinas/disciplina_form.html", disciplina=None)
        
        pagination, usuario_admin = criar_paginacao(request, Disciplina, current_user, 'id', True)
        return render_template('disciplinas/disciplinas_list.html',
                           disciplinas=pagination.items, 
                           pagination=pagination,
                           is_admin=usuario_admin)
          

    def post(self, id=None):
        
        nome_disciplina = request.form.get('nome')

        if request.endpoint == 'disciplinas.disciplina_excluir':
            sucesso, erro = delete_disciplina(id)

            if sucesso:
                flash('Disciplina excluída com sucesso!', 'success')
            else:
                flash('Não foi possível excluir a disciplina.', 'error')
            
            return redirect(url_for('disciplinas.disciplina_view'))
        
        if id is None:
          sucesso, erro = create_disciplina(nome_disciplina, current_user.id)
          mensagem_sucesso = 'Disciplina criada com sucesso!'        
        else:
          sucesso, erro = edit_disciplina(id, nome_disciplina)
          mensagem_sucesso = 'Disciplina atualizada com sucesso!'
          
        if sucesso:
            flash(mensagem_sucesso, 'success')
            return redirect(url_for('disciplinas.disciplina_view'))
          
     
        flash(f'Erro: {erro}', 'error')
        disciplina_atual = {'id': id, 'nome': nome_disciplina}

        return render_template('disciplinas/disciplina_form.html', disciplina=disciplina_atual)      

        