from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

app = Flask(__name__)

# PostgreSQL Veritabanı Bağlantısı
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://kullanici:şifre@hostname:port/dbname"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Kullanıcı Modeli (Tablo)
class Kullanici(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    sifre = db.Column(db.String(200), nullable=False)

# Veritabanını Başlat
with app.app_context():
    db.create_all()

# Kullanıcı Kayıt
@app.route('/register', methods=['POST'])
def register():
    veri = request.json
    email = veri.get("email")
    sifre = veri.get("sifre")

    # Kullanıcı zaten var mı?
    if Kullanici.query.filter_by(email=email).first():
        return jsonify({"hata": "Bu e-posta zaten kayıtlı!"}), 400

    # Şifreyi hashle ve kaydet
    sifre_hashli = bcrypt.generate_password_hash(sifre).decode("utf-8")
    yeni_kullanici = Kullanici(email=email, sifre=sifre_hashli)
    db.session.add(yeni_kullanici)
    db.session.commit()

    return jsonify({"mesaj": "Kullanıcı başarıyla oluşturuldu!"}), 201

# Kullanıcı Giriş
@app.route('/login', methods=['POST'])
def login():
    veri = request.json
    email = veri.get("email")
    sifre = veri.get("sifre")

    kullanici = Kullanici.query.filter_by(email=email).first()

    if kullanici and bcrypt.check_password_hash(kullanici.sifre, sifre):
        token = create_access_token(identity=email)
        return jsonify({"mesaj": "Giriş başarılı", "token": token})

    return jsonify({"hata": "Geçersiz e-posta veya şifre"}), 401

if __name__ == '__main__':
    app.run(debug=True)
