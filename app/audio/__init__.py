from flask import Blueprint


audio = Blueprint('audio', __name__)

# we import audio views here to avoid circular dependancy issues
from . import views 


