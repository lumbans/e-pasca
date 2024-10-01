# app.py
from flask import Flask
from config import Config
from routes.auth_routes import auth_bp
from routes.common_routes import common_bp

# Import blueprints
from routes.auth_routes import auth_bp
from routes.pelanggan_routes import pelanggan_bp
from routes.tagihan_routes import tagihan_bp
from routes.pembayaran_routes import pembayaran_bp
from routes.tarif_routes import tarif_bp
from routes.report_routes import report_bp
from routes.common_routes import common_bp
from routes.user_routes import user_bp
from routes.error_handlers import error_bp

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY
app.config.from_object('config.Config')

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(pelanggan_bp, url_prefix='/pelanggan')
app.register_blueprint(tagihan_bp, url_prefix='/tagihan')
app.register_blueprint(pembayaran_bp, url_prefix='/pembayaran')
app.register_blueprint(tarif_bp, url_prefix='/tarif')
app.register_blueprint(report_bp, url_prefix='/reports')
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(common_bp)
app.register_blueprint(error_bp)  # Register error handlers blueprint

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
