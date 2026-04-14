from . import escolas_bp
from .views import EscolaView

escolas_bp.add_url_rule('/escolas', 
                     view_func=EscolaView.as_view('escolas_view'), 
                     methods=['GET', 'POST'])
    

escolas_bp.add_url_rule('/escolas/novo', 
                 view_func=EscolaView.as_view('escola_create'), 
                 methods=['GET', 'POST'])

escolas_bp.add_url_rule('/escolas/edit/<int:id>', 
                 view_func=EscolaView.as_view('escola_edit'), 
                 methods=['GET', 'POST'])

escolas_bp.add_url_rule('/escolas/excluir/<int:id>', 
                     view_func=EscolaView.as_view('escola_excluir'), 
                     methods=['GET', 'POST', 'DELETE'])