from flask import Blueprint

aulas_bp = Blueprint(
    'aulas',
    __name__,
    template_folder='templates'
)

from . import urls

