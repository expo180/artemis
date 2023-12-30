from flask import Flask
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from conf import config
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_restcountries import CountriesAPI
from flask_migrate import Migrate
from flask_babel import Babel, gettext

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
bootstrap = Bootstrap()
mail = Mail()
babel = Babel()
db = SQLAlchemy()
moment = Moment()
rapi = CountriesAPI()
migrate = Migrate()

def create_app(development=True):
    app = Flask(__name__)
    app.config.from_object(config['development'])
    app.config['LANGUAGES'] = ['en', 'fr', 'ja', 'ar', 'it', 'es', 'pt', 'ru', 'pl']
    app.config['BABEL_DEFAULT_LOCALE'] = 'en'
    config['development'].init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)
    login_manager.init_app(app)
    rapi.init_app(app)
    babel.init_app(app)

    # Register blueprints
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    with app.app_context():
        # Create database tables and insert roles
        db.create_all()
        from app.models import Role
        Role.insert_roles()

    return app
