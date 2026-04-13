from . import estrutura_bp
from .views import EstuturaViewCiclos, EstuturaViewSerie


estrutura_bp.add_url_rule('/estruturas',
                          view_func=EstuturaViewSerie.as_view('estrutura_view'),
                          methods=['GET', 'POST'])

estrutura_bp.add_url_rule('/estrutura/serie/novo',
                          view_func=EstuturaViewSerie.as_view('estrutura_create_serie'),
                          methods=['GET', 'POST'])

estrutura_bp.add_url_rule('/estrutura/serie/edit/<int:id>',
                          view_func=EstuturaViewSerie.as_view('estrutura_edit_serie'),
                          methods=['GET', 'POST'])

estrutura_bp.add_url_rule('/estrutura/serie/delete/<int:id>',
                          view_func=EstuturaViewSerie.as_view('estrutura_serie_delete'))


estrutura_bp.add_url_rule('/estrutura/ciclos/novo',
                          view_func=EstuturaViewCiclos.as_view('estrutura_create_ciclos'),
                          methods=['GET', 'POST'])

estrutura_bp.add_url_rule('/estrutura/ciclos/edit/<int:id>',
                          view_func=EstuturaViewCiclos.as_view('estrutura_edit_ciclos'),
                          methods=['GET', 'POST'])

estrutura_bp.add_url_rule('/estrutura/ciclos/delete/<int:id>',
                          view_func=EstuturaViewCiclos.as_view('estrutura_delete_ciclos'))