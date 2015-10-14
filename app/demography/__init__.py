from flask import Blueprint

demography = Blueprint('demography', __name__)

from . import views, errors
from ..spandex.models import Permission


@demography.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
