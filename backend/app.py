from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from routes.auth_routes import auth_routes
from routes.usage_routes import usage_routes
from routes.tagihan_routes import tagihan_routes
from routes.pelanggan_routes import pelanggan_routes
from routes.pembayaran_routes import pembayaran_routes
from dotenv import load_dotenv
import os

load_dotenv() 

app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = 'your-secret-key'
jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(auth_routes)
app.register_blueprint(usage_routes)
app.register_blueprint(tagihan_routes)
app.register_blueprint(pelanggan_routes)
app.register_blueprint(pembayaran_routes)

if __name__ == '__main__':
    app.run(debug=True)
