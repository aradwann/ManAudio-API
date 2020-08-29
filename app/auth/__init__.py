from flask import Blueprint


auth = Blueprint('auth', __name__)

# we import auth views here to avoid circular dependancy issues
from . import views 


