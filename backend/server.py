from flask import Flask, request, jsonify
from flask_cors import CORS  
from models import db
from routes import register, login
from module.Preprocessing import TextProcessor
from module.AnalysisService import TextClassifier
import pandas as pd

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/sentivote'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Register Blueprints
app.register_blueprint(register)
app.register_blueprint(login)

# Create an instance of TextProcessor and TextClassifier
text_processor = TextProcessor()
text_classifier = TextClassifier()

# Define allowed file extensions
ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/analisis', methods=['POST'])
def upload_csv():
    try:
        file = request.files['file']

        if file and allowed_file(file.filename):
            # Read CSV into a DataFrame
            df = pd.read_csv(file)

            # Preprocessing using the TextProcessor
            df['preprocessed'] = df['Text Tweet'].apply(text_processor.preprocess_all)
            
            # Extract features using the TextClassifier
            tfidf_matrix = text_classifier.train_tfidf(df["preprocessed"])
            selected_features = text_classifier.select_features_chi2(tfidf_matrix, df['Pasangan Calon'])

            # Train the Random Forest classifier
            best_rf_model = text_classifier.train_rf(selected_features, df['Pasangan Calon'])

            # Predict using the trained model
            df['prediction'] = best_rf_model.predict(selected_features)

            # Return the processed DataFrame with predictions as JSON
            return jsonify(df.to_dict(orient='records'))
        else:
            return jsonify({'error': 'Invalid file or file type'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Running app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Buat tabel di database sebelum menjalankan aplikasi
    app.run(debug=True)