# from src import db 
# from src.routes.routes import inventory_bp
# from flask import Flask
# from flask_cors import CORS
# import yaml, os
# from src.config.settings import get_refresh_interval

# def create_app():
#     app = Flask(__name__)
    
#     # Enable CORS for all routes
#     CORS(app)

#     @app.route('/')  
#     def hello():
#         return "Hello World!"

#     # Load config.yaml
#     base_dir = os.path.dirname(os.path.abspath(__file__))
#     config_path = os.path.join(base_dir, 'src', 'config', 'config.yaml')

#     with open(config_path, 'r') as f:
#         config = yaml.safe_load(f)

#     env = os.getenv('ENV', 'DEVELOPMENT')
#     db_uri = config[env]['DATABASE_URI']

#     app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#     app.config['REFRESH_INTERVAL_MINUTES'] = get_refresh_interval()

#     db.init_app(app)
#     app.register_blueprint(inventory_bp)  

#     return app

# #  allows `flask run` to discover the app
# app = create_app()


from src import db
from src.routes.routes import inventory_bp
from flask import Flask
from flask_cors import CORS
import yaml, os
from src.config.settings import get_refresh_interval

def create_app():
    app = Flask(__name__)

    CORS(
        app,
        resources={r"/api/*": {"origins": "*"}},
        supports_credentials=True
    )

    @app.route('/')
    def hello():
        return "Hello World!"

    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Existing config.yaml
    config_path = os.path.join(
        base_dir,
        'src',
        'config',
        'config.yaml'
    )

    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    # NEW: auth.yaml
    auth_path = os.path.join(
        base_dir,
        'src',
        'config',
        'auth.yaml'
    )

    with open(auth_path, 'r', encoding='utf-8') as f:
        auth_config = yaml.safe_load(f)

    # Store password in app config
    # app.config['PERMISSION_PASSWORD'] = auth_config['permission']['password']
    app.config["PERMISSION_PASSWORD_HASH"] = (
       auth_config["permission"]["password_hash"]
    )

    env = os.getenv('ENV', 'DEVELOPMENT')
    db_uri = config[env]['DATABASE_URI']

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['REFRESH_INTERVAL_MINUTES'] = get_refresh_interval()

    db.init_app(app)
    app.register_blueprint(inventory_bp)

    return app

app = create_app()
