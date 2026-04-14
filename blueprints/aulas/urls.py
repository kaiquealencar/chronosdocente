from . import aulas_bp
from .views import AulaView


aulas_bp.add_url_rule('/aulas',
                      view_func=AulaView.as_view('aulas_view'),
                      methods=['GET', 'POST'])

aulas_bp.add_url_rule('/aulas/novo',
                      view_func=AulaView.as_view('aulas_create'),
                      methods=['GET', 'POST'])


aulas_bp.add_url_rule('/aulas/edit/<int:id>',
                      view_func=AulaView.as_view('aulas_edit'),
                      methods=['GET', 'POST'])


aulas_bp.add_url_rule('/aulas/delete/<int:id>',
                      view_func=AulaView.as_view('aulas_delete'),
                      methods=['GET', 'POST'])


