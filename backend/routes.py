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

# Menggunakan model RF Aspek 
rf_aspect_model = joblib.load('./module/machine/rf_aspect_model.joblib')
tfidf_vectorizer = joblib.load('./module/machine/tfidf_vectorizer.joblib')
chi2_selector = joblib.load('./module/machine/chi2_selector.joblib')

# Menggunakan model RF Agus
rf_agus_model = joblib.load('./module/machine/rf_agus_model.joblib')
tfidf_vectorizer_agus = joblib.load('./module/machine/tfidf_vectorizer_agus.joblib')
chi2_selector_agus = joblib.load('./module/machine/chi2_selector_agus.joblib')

# Menggunakan model RF Ahok
rf_ahok_model = joblib.load('./module/machine/rf_ahok_model.joblib')
tfidf_vectorizer_ahok = joblib.load('./module/machine/tfidf_vectorizer_ahok.joblib')
chi2_selector_ahok = joblib.load('./module/machine/chi2_selector_ahok.joblib')

# Menggunakan model RF Anies
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
            X_new_tfidf_ahok = tfidf_vectorizer_ahok.transform([preprocessed_text])
            X_new_tfidf_agus = tfidf_vectorizer_agus.transform([preprocessed_text])
            X_new_tfidf_anies = tfidf_vectorizer_anies.transform([preprocessed_text])

            # Use the same chi-square selector
            X_new_chi2_ahok = chi2_selector_ahok.transform(X_new_tfidf_ahok)
            X_new_chi2_agus = chi2_selector_agus.transform(X_new_tfidf_agus)
            X_new_chi2_anies = chi2_selector_anies.transform(X_new_tfidf_anies)

            # Predict probabilities using the three models
            prob_ahok = rf_ahok_model.predict_proba(X_new_chi2_ahok)[0]
            prob_agus = rf_agus_model.predict_proba(X_new_chi2_agus)[0]
            prob_anies = rf_anies_model.predict_proba(X_new_chi2_anies)[0]

            # Choose the model with the highest probability
            chosen_model = max([(prob_ahok[1], 'ahok'), (prob_agus[1], 'agus'), (prob_anies[1], 'anies')], key=lambda x: x[0])

            # Get the chosen model
            if chosen_model[1] == 'ahok':
                prediction_sentiment = rf_ahok_model.predict(X_new_chi2_ahok)[0]
            elif chosen_model[1] == 'agus':
                prediction_sentiment = rf_agus_model.predict(X_new_chi2_agus)[0]
            elif chosen_model[1] == 'anies':
                prediction_sentiment = rf_anies_model.predict(X_new_chi2_anies)[0]

            # TF-IDF vectorizer and chi-square selector for aspect analysis
            X_new_tfidf_aspect = tfidf_vectorizer.transform([preprocessed_text])
            X_new_chi2_aspect = chi2_selector.transform(X_new_tfidf_aspect)

            # Predict aspect using rf_aspect_model
            prediction_aspect = rf_aspect_model.predict(X_new_chi2_aspect)[0]
            
            # Menambahkan hasil prediksi ke dalam respons
            response_data = {
                "result": preprocessed_text,
                "chosen_model": chosen_model[1],
                "prediction_sentiment": prediction_sentiment,
                "prediction_confidence": chosen_model[0],
                "prediction_aspect": prediction_aspect
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
