from flask import Flask, request, jsonify
from flask_cors import CORS  
from flask_jwt_extended import JWTManager
from models import db
from routes import register, login, predict, predictFile
import joblib

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/sentivote'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'sentivote-app'
app.config['JWT_SECRET_KEY'] = 'sentivote-app'
db.init_app(app)

jwt = JWTManager()
jwt.init_app(app)

# Menggunakan model RF agus yang telah dimuat
# rf_agus_model = joblib.load('./module/machine/rf_agus_model.joblib')
# rf_ahok_model = joblib.load('./module/machine/rf_ahok_model.joblib')
rf_anies_model = joblib.load('./module/machine/rf_anies_model.joblib')

# Register Blueprints
app.register_blueprint(register)
app.register_blueprint(login)
app.register_blueprint(predict)
app.register_blueprint(predictFile)

# Running app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(debug=True)