from flask import Blueprint

eol = Blueprint('eol', __name__)

from . import views, errors
from ..models import Permission, Plant, Species


@demography.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
