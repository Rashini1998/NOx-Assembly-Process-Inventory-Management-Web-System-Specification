from src import db  # db is initialized in src/__init__.py
from src.routes.routes import inventory_bp
from flask import Flask
from flask_cors import CORS
import yaml, os


def create_app():
    app = Flask(__name__)
    
    # Enable CORS for all routes
    CORS(app)

    @app.route('/')  
    def hello():
        return "Hello World!"

    # Load config.yaml
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, 'src', 'config', 'config.yaml')

    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    env = os.getenv('ENV', 'DEVELOPMENT')
    db_uri = config[env]['DATABASE_URI']

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    app.register_blueprint(inventory_bp)  

    return app

#  allows `flask run` to discover the app
app = create_app()
