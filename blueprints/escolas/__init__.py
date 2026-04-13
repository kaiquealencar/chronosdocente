from flask import Blueprint

escolas_bp = Blueprint(
    'escolas',
    __name__,
    template_folder='templates'
)


from . import urls