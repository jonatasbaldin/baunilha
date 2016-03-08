from flask import Flask

# creates an app and import its configuration
app = Flask(__name__, instance_relative_config=True)
# loads config.Class
app.config.from_object('config.ProductionConfig')
# loads instance/config.py
app.config.from_pyfile('config.py')

# circular import
# the views depend on a configured app
from baunilha import views
