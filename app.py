from flask import Flask
from flask_cors import CORS
from config.config import Config
import firebase_set
from models.user import db
from routes.routes import initialize_routes

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # Load configuration
    app.config.from_object(Config)
    
    # Initialize Firebase
    firebase_set.initialize_firebase()
    
    # Initialize SQLAlchemy (or another database)
    db.init_app(app)
    
    # Initialize routes
    initialize_routes(app)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
