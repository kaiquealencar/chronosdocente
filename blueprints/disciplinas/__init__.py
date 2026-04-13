from flask import Blueprint

disciplinas_bp = Blueprint(
    'disciplinas',
      __name__,
      template_folder='templates'
      
    )

from . import urls