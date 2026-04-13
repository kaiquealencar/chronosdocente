from flask import Blueprint

estrutura_bp = Blueprint(
    'estruturas',
    __name__,
    template_folder='templates'
)


from . import urls