from datetime import datetime
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from flask.views import MethodView
from sqlalchemy.orm import joinedload

from utils.decorator import escola_pertence_ao_usuario
from utils.pagination import criar_paginacao
from models.aula import Aula
from repositories.aula_repository import create_aula, edit_aula, delete_aula

from models.disciplina import Disciplina
from models.escola import Escola
from models.serie import Serie

class AulaView(MethodView):
    decorators = [login_required]

    def get(self, id=None):
         
        if request.endpoint in ['aulas.aulas_create', 'aulas.aulas_edit']:
            aula = None

            if id:
                aula = Aula.query.get_or_404(id) 
                if not current_user.is_admin and aula.usuario_id != current_user.id:
                     flash('Acesso negado', 'danger')
                     return redirect(url_for('aulas.aulas_view'))
                
            
            escolas = Escola.query.filter_by(usuario_id=current_user.id).all()
            disciplinas = Disciplina.query.filter_by(usuario_id=current_user.id).all()
            series = Serie.query.filter_by(usuario_id=current_user.id).all()
                
            return render_template(
                'aulas/form_aula.html', 
                aula=aula,
                escolas=escolas,
                series=series,
                disciplinas=disciplinas
            )
               
        opcoes_otimizacao = [joinedload(Aula.disciplina), joinedload(Aula.escola)]
        pagination, usuario_admin = criar_paginacao(request, Aula, current_user, 'dia_aula', True, options=opcoes_otimizacao)
         
        return render_template('aulas/list_aulas.html',
                                aulas=pagination.items,
                                pagination=pagination,
                                is_admin=usuario_admin)
                    
                
         


    def post(self, id=None):
        if request.endpoint == 'aulas.aulas_delete':
            sucesso, erro = delete_aula(id)
            if sucesso:
                flash('Aula removida com sucesso!', 'success')
            else:
                flash(f'Erro ao excluir: {erro}', 'error')
            return redirect(url_for('aulas.aulas_view'))

        try:
            dia_aula = datetime.strptime(request.form.get('dia_aula'), '%Y-%m-%d').date()
            hora_inicio = datetime.strptime(request.form.get('hora_inicio'), '%H:%M').time()
            hora_fim = datetime.strptime(request.form.get('hora_fim'), '%H:%M').time()
            quantidade_aulas = int(request.form.get('quantidade_aulas'))
            
            disciplina_id = int(request.form.get('disciplina_id'))
            escola_id = int(request.form.get('escola_id'))
            serie_id = int(request.form.get('serie_id'))
            usuario_id = current_user.id
        except (ValueError, TypeError) as e:
            flash('Dados inválidos ou campos obrigatórios ausentes.', 'error')
            return redirect(request.referrer)

        if id is None:
            sucesso, erro = create_aula(
                dia_aula, hora_inicio, hora_fim, quantidade_aulas, 
                disciplina_id, usuario_id, escola_id, serie_id
            )
            mensagem = 'Aula agendada com sucesso!'
        else:
            sucesso, erro = edit_aula(
                id, dia_aula, hora_inicio, hora_fim, quantidade_aulas,
                disciplina_id, usuario_id, escola_id, serie_id
            )
            mensagem = 'Aula atualizada com sucesso!'

        if sucesso:
            flash(mensagem, 'success')
            return redirect(url_for('aulas.aulas_view'))
        
        flash(f'Erro: {erro}', 'error')
        
        aula_refill = {
            'id': id, 
            'dia_aula': dia_aula,
            'hora_inicio': hora_inicio,
            'hora_fim': hora_fim,
            'disciplina_id': disciplina_id,
            'escola_id': escola_id,
            'serie_id': serie_id,
            'quantidade_aulas': quantidade_aula 
        }
        
        disciplinas = Disciplina.query.filter_by(usuario_id=current_user.id).all()
        escolas = Escola.query.filter_by(usuario_id=current_user.id).all()
        series = Serie.query.filter_by(usuario_id=current_user.id).all()

        return render_template('aulas/form_aula.html', 
                               aula=aula_refill, 
                               disciplinas=disciplinas, 
                               escolas=escolas, 
                               series=series)         
    

