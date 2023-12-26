from flask import Flask
from flask_cors import CORS  
from models import db
from routes import register, login

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/sentivote'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Register Blueprints
app.register_blueprint(register)
app.register_blueprint(login)

# Running app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Buat tabel di database sebelum menjalankan aplikasi
    app.run(debug=True)
