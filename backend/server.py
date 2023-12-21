# app.py (Flask application)

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import pickle
import pandas as pd

app = Flask(__name__)
CORS(app, resources={r"/analisis": {"origins": "http://localhost:5173"}}, supports_credentials=True, methods=["POST"])

# Load model preprocessing
model_path = os.path.join(os.path.dirname(__file__), 'model', 'text_processor.sav')

class TextProcessor:
    def __init__(self):
        # Initialization logic, if any
        pass

    def preprocess(self, text):
        # Placeholder for preprocessing logic
        # Customize this method based on your model's requirements
        return text

# Load TextProcessor model
with open(model_path, 'rb') as f:
    text_processor_model = pickle.load(f)

print("Model berhasil dimuat. Path:", os.path.abspath(f.name))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'csv'}

@app.route('/analisis', methods=['POST'])
def upload_csv():
    try:
        file = request.files['file']

        if file and allowed_file(file.filename):
            # Read CSV into a DataFrame
            df = pd.read_csv(file)

            # Preprocessing using the TextProcessor
            text_processor = TextProcessor()
            df['preprocessed'] = df['Text Tweet'].apply(text_processor.preprocess)
            df['tokenized'] = df['preprocessed'].apply(lambda x: x.split())

            # Return the processed DataFrame as JSON
            return jsonify(df.to_dict(orient='records'))
        else:
            return jsonify({'error': 'Invalid file or file type'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
