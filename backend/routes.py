from flask import Blueprint, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from models import db, User, UserSchema,AnalysisResult
from sqlalchemy.exc import IntegrityError
from module.Preprocessing import Preprocessing
from module.Classifier import Classifier
from module.SentimentClassifier import SentimentClassifier
import pandas as pd
import joblib

bcrypt = Bcrypt()
jwt = JWTManager()

register = Blueprint('register', __name__)
login = Blueprint('login', __name__)
predict = Blueprint('predict', __name__)
predictFile = Blueprint('predictFile', __name__)

user_schema = UserSchema()
preprocessor = Preprocessing() 
text_classifier = Classifier()

# Menggunakan model RF
rf_anies_model = joblib.load('./module/machine/rf_anies_model.joblib')
tfidf_vectorizer_anies = joblib.load('./module/machine/tfidf_vectorizer_anies.joblib')
chi2_selector_anies = joblib.load('./module/machine/chi2_selector_anies.joblib')

# Define allowed file extensions
ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@register.route('/register', methods=['POST'])
def register_user():
    data = request.json
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], email=data['email'], password=hashed_password)

    try:
        db.session.add(new_user)
        db.session.commit()
        return user_schema.jsonify(new_user)
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Username or email already exists'}), 400

@login.route('/login', methods=['POST'])
def login_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        return jsonify({'success': True, 'access_token': access_token, 'message': 'Login successful'})
    else:
        return jsonify({'success': False, 'message': 'Invalid username or password'}), 401

@predict.route('/analisis/input-teks', methods=['POST'])
def preprocess_text():
    if request.method == 'POST':
        data = request.get_json()
        text_to_preprocess = data.get('text')

        if text_to_preprocess:
            preprocessed_text = preprocessor.preprocess_all(text_to_preprocess)

            # Use the same TF-IDF vectorizer
            X_new_tfidf = tfidf_vectorizer_anies.transform([preprocessed_text])

            # Use the same chi-square selector
            X_new_chi2 = chi2_selector_anies.transform(X_new_tfidf)

            # Lakukan prediksi menggunakan model RF yang telah dimuat 
            prediction = rf_anies_model.predict(X_new_chi2)[0]
            
            # Menambahkan hasil prediksi ke dalam respons
            response_data = {
                "result": preprocessed_text,
                "prediction": prediction
            }

            return jsonify(response_data)
        else:
            return jsonify({"error": "Missing 'text' parameter"}), 400
    else:
        return jsonify({"error": "Unsupported method"}), 405

    
@predictFile.route('/analisis', methods=['POST'])
def preprocess_file():
    try:
        file = request.files['file']

        if file and allowed_file(file.filename):
            # Read CSV into a DataFrame
            df = pd.read_csv(file)

            # Preprocessing using the TextProcessor
            df['preprocessed'] = df['Text Tweet'].apply(preprocessor.preprocess_all)
            
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

            # Simpan hasil analisis ke dalam database berdasarkan pasangan calon
            for index, row in df.iterrows():
                pasangan_calon = row['Pasangan Calon']
                result = AnalysisResult(
                    data=row['preprocessed'],
                    aspek=row['prediction'],
                    sentiment=row['sentiment prediction']
                    # Tambahkan kolom lain sesuai kebutuhan
                )
                db.session.add(result)

            # Commit perubahan ke dalam database
            db.session.commit()

            # Return the processed DataFrame with predictions as JSON
            return jsonify(df.to_dict(orient='records'))
        else:
            return jsonify({'error': 'Invalid file or file type'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

if __name__ == '__main__':
    app.run(debug=True)
