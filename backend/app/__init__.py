from flask_cors import CORS
from flask import Flask 
from flask_jwt_extended import JWTManager 
from .config import Config
from .db import init_db
from .auth import auth_bp
from .notes import notes_bp 


jwt= JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app, resources={r"/*":{"origins":"*"}},
         supports_credentials= True)


    jwt.init_app(app)

    

    app.register_blueprint(auth_bp)
    app.register_blueprint(notes_bp)

    with app.app_context():
        init_db()

    return app


