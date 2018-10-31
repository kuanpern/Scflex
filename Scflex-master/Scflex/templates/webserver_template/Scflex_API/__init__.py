import yaml
import flask
from flask import Flask
from flask_mail import Mail
from flask_mongoengine import MongoEngine
from flask_security import Security, MongoEngineUserDatastore, UserMixin, RoleMixin, login_required, current_user

# read from confiration file
config_filename = '/home/user/.keys/Scflex_server.yaml'
configs = yaml.load(open(config_filename))

# Create app
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = configs['SECRET']

# Email configuration
app.config.update(configs['EMAIL_CONFIGS'])

# MongoDB Config
app.config['MONGODB_SETTINGS'] = configs['MONGODB_SETTINGS']

# website configuration
app.config['SECURITY_REGISTERABLE'] = True
#app.config['SECURITY_CONFIRMABLE' ] = True
app.config['SECURITY_RECOVERABLE' ] = True
app.config['SECURITY_CHANGEABLE'  ] = True

# Create database connection object
db = MongoEngine(app)

class Role(db.Document, RoleMixin):
	name         = db.StringField(max_length=80, unique=True)
	description  = db.StringField(max_length=255)
# end class

class User(db.Document, UserMixin):
	name         = db.StringField(max_length=255)
	email        = db.StringField(max_length=255)
	password     = db.StringField(max_length=255)
	active       = db.BooleanField(default=True)
	roles        = db.ListField(db.ReferenceField(Role), default=[])
	confirmed_at = db.DateTimeField()
# end class

# Setup Flask-Security
user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Create a user to test with
@app.before_first_request
def create_user():
	user_datastore.create_user(name='root', email='root@scflex.com', password='password')
# end def

# Import views
import Scflex_API.views.default
