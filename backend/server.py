from flask import Flask, request, jsonify
from flask_cors import CORS  
from flask_jwt_extended import JWTManager
from models import db
from routes import register, login
from module.Preprocessing import TextProcessor
from module.AnalysisService import TextClassifier
from module.SentimentClassifier import SentimentClassifier
import pandas as pd

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

            sentiment_classifier_agus = SentimentClassifier(df, "Agus-Sylvi")
            df_agus = sentiment_classifier_agus.get_df_calon ()
            tfidf_matrix_agus = sentiment_classifier_agus.get_X_new()
            best_rf_model_agus = text_classifier.train_rf(tfidf_matrix_agus, df_agus['Sentiment'])
            df.loc[df['Pasangan Calon'] == 'Agus-Sylvi', 'sentiment prediction'] = best_rf_model_agus.predict(tfidf_matrix_agus)

            sentiment_classifier_ahok = SentimentClassifier(df, "Ahok-Djarot")
            df_ahok = sentiment_classifier_ahok.get_df_calon ()
            tfidf_matrix_ahok = sentiment_classifier_ahok.get_X_new()
            best_rf_model_ahok = text_classifier.train_rf(tfidf_matrix_ahok, df_ahok['Sentiment'])
            df.loc[df['Pasangan Calon'] == 'Ahok-Djarot', 'sentiment prediction'] = best_rf_model_ahok.predict(tfidf_matrix_ahok)

            sentiment_classifier_anies = SentimentClassifier(df, "Anies-Sandi")
            df_anies = sentiment_classifier_anies.get_df_calon ()
            tfidf_matrix_anies = sentiment_classifier_anies.get_X_new()
            best_rf_model_anies = text_classifier.train_rf(tfidf_matrix_anies, df_anies['Sentiment'])
            df.loc[df['Pasangan Calon'] == 'Anies-Sandi', 'sentiment prediction'] = best_rf_model_anies.predict(tfidf_matrix_anies)

            # Return the processed DataFrame with predictions as JSON
            return jsonify(df.to_dict(orient='records'))
        else:
            return jsonify({'error': 'Invalid file or file type'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Running app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(debug=True)