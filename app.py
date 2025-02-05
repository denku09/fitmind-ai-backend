from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config
from models import db
from routes import routes

app = Flask(__name__)
app.config.from_object(Config)

# CORS, JWT ve Veritabanı yapılandırma
CORS(app)
db.init_app(app)
jwt = JWTManager(app)

# API endpointlerini Blueprint olarak bağla
app.register_blueprint(routes)

# Veritabanını başlat
with app.app_context():
    db.create_all()

# Ana çalışma dosyası
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
