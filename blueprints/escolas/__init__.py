from flask import Blueprint

escolas_bp = Blueprint('escolas', __name__)

from . import urls