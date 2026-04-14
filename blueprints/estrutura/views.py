from flask import render_template, request, redirect, url_for, flash, abort
from flask.views import MethodView
from flask_login import login_required, current_user
from extensions import db
from models.serie import Ciclo, Serie
from models.escola import Escola

from repositories.estrutura_ciclos_repository import create_ciclos, edit_ciclos, delete_ciclo 
from repositories.estrutura_serie_repository import create_serie, edit_serie, delete_serie


class EstuturaViewCiclos(MethodView):
    decorators = [login_required]

    def get(self, id=None):
        escolas = Escola.query.filter_by(usuario_id=current_user.id).all()
        
        if id:
            ciclo = db.session.get(Ciclo, id)
            if not ciclo or ciclo.usuario_id != current_user.id:
                abort(403)
            return render_template('estruturas/form_ciclo.html', ciclo=ciclo, escolas=escolas)
        
        return render_template('estruturas/form_ciclo.html', ciclo=None, escolas=escolas)

    def post(self, id=None):
        if "delete" in request.endpoint:
            ciclo = db.session.get(Ciclo, id)
            if not ciclo or ciclo.usuario_id != current_user.id:
                abort(403)
            
            sucesso, erro = delete_ciclo(id)
            if sucesso:
                flash("Ciclo excluído com sucesso!", "success")
            else:
                flash(f"Erro ao excluir: {erro}", "danger")
            return redirect(url_for('estruturas.estrutura_view'))

        nome = request.form.get('nome')
        escola_id = request.form.get('escola_id')
        ordem = request.form.get('ordem', type=int) or 1

        if id: 
            ciclo = db.session.get(Ciclo, id)
            if not ciclo or ciclo.usuario_id != current_user.id:
                abort(403)
            sucesso, erro = edit_ciclos(id, nome, ordem)
        else: 
            sucesso, erro = create_ciclos(nome, escola_id, current_user.id, ordem)

        if sucesso:
            flash("Ciclo salvo com sucesso!", "success")
            return redirect(url_for('estruturas.estrutura_view'))
        
        flash(f"Erro ao salvar ciclo: {erro}", "danger")
        return redirect(request.referrer)


class EstuturaViewSerie(MethodView):
    decorators = [login_required]

    def get(self, id=None):
        ciclos = Ciclo.query.filter_by(usuario_id=current_user.id)\
            .order_by(Ciclo.ordem).all()
        
        if request.endpoint == 'estruturas.estrutura_create_serie':
            print(f'Recebeu o click do botão. ENDPOINT: {request.url}')
            return render_template('estruturas/form_serie.html', ciclos=ciclos)        
        
        if id is None:
            ciclos_ids = [c.id for c in ciclos]

            series = Serie.query.filter(
                Serie.ciclo_id.in_(ciclos_ids)
            ).all() if ciclos_ids else []

            return render_template(
                'estruturas/lista_estrutura.html',
                ciclos=ciclos,
                series=series
            )                

        serie = Serie.query.get_or_404(id)
        return render_template('estruturas/form_serie.html', serie=serie, ciclos=ciclos)  



    
    def post(self, id=None):
        if request.endpoint == 'estruturas.estrutura_serie_delete':
            serie = db.session.get(Serie, id)
            if not serie or serie.usuario_id != current_user.id:
                abort(403)
            
            sucesso, erro = delete_serie(id)
            if sucesso:
                flash("Série excluída com sucesso!", "success")
            else:
                flash(f"Erro ao excluir: {erro}", "danger")
            return redirect(url_for('estruturas.estrutura_view'))

        nome = request.form.get('nome')
        ciclo_id = request.form.get('ciclo_id', type=int)

        if id:
            serie = db.session.get(Serie, id)
            print(serie.nome, serie.ciclo_id, type(serie.ciclo_id))

            if not serie or (serie.usuario_id != current_user.id and not current_user.is_admin):
                flash("Acesso negado ou série inexistente.", "error")
                return redirect(url_for('series.serie_view'))

           
            sucesso, erro = edit_serie(id, nome, ciclo_id)
        else: 
            ciclo_pai = db.session.get(Ciclo, ciclo_id)
            if not ciclo_pai or ciclo_pai.usuario_id != current_user.id:
                flash("Ciclo inválido.", "danger")
                return redirect(request.referrer)
                
            sucesso, erro = create_serie(nome, ciclo_id, ciclo_pai.escola_id, current_user.id)

        if sucesso:
            flash("Série salva com sucesso!", "success")
            return redirect(url_for('estruturas.estrutura_view'))
        
        flash(f"Erro ao salvar série: {erro}", "danger")
        return redirect(request.referrer)