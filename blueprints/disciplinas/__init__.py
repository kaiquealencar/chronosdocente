from flask import Blueprint

disciplinas_bp = Blueprint('disciplinas', __name__)

from . import urls