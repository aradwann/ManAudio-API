from flask import Blueprint, current_app


audio = Blueprint('audio', __name__)

# we import audio views here to avoid circular dependancy issues
from . import views 


