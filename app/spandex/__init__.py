from flask import Blueprint

spandex = Blueprint('spandex', __name__, template_folder='./templates')

from . import views, errors, models
from .models import Permission


@spandex.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
