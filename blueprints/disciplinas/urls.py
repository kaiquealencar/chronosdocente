from . import disciplinas_bp
from .views import DisciplinaView


disciplinas_bp.add_url_rule('/disciplinas', 
                     view_func=DisciplinaView.as_view('disciplina_view'),
                     methods=['GET', 'POST']
                     )
    
disciplinas_bp.add_url_rule('/disciplina/novo',
                     view_func=DisciplinaView.as_view('disciplina_create'),
                     methods=['GET', 'POST'])

disciplinas_bp.add_url_rule('/disciplina/edit/<int:id>',
                     view_func=DisciplinaView.as_view('disciplina_edit'),
                     methods=['GET', 'POST'])
    
disciplinas_bp.add_url_rule('/disciplina/delete/<int:id>',
                     view_func=DisciplinaView.as_view('disciplina_excluir'),
                     methods=['GET', 'POST'])