from . import usuarios_bp
from .views import UsuarioView

usuarios_bp.add_url_rule('/usuarios', 
                         view_func=UsuarioView.as_view('usuario_view'),
                         methods=['GET', 'POST'])

usuarios_bp.add_url_rule('/usuario/novo',
                         view_func=UsuarioView.as_view('usuario_create'),
                         methods=['GET', 'Post'])

usuarios_bp.add_url_rule('/usuario/edit/<int:id>',
                         view_func=UsuarioView.as_view('usuario_edit'),
                         methods=['GET', 'POST'])

usuarios_bp.add_url_rule('/usuario/delete/<int:id>',
                         view_func=UsuarioView.as_view('usuario_delete'),
                         methods=['GET', 'POST'])

