from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from text_processor import TextProcessor  # Sesuaikan dengan struktur proyek Anda
import pickle

app = Flask(__name__)
CORS(app, resources={r"/analyze": {"origins": "http://localhost:5173"}, "/*": {"origins": "http://localhost:5173"}})

# Load model preprocessing
with open('model/text_processor.sav', 'rb') as f:
    text_processor_model = pickle.load(f)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'csv'}

@app.route('/upload-csv', methods=['POST'])
def upload_csv():
    file = request.files['file']

    if file and allowed_file(file.filename):
        # Baca CSV ke dalam DataFrame
        df = pd.read_csv(file)

        # Preprocessing kolom 'Text Tweet' menggunakan model TextProcessor
        df['preprocessed'] = df['Text Tweet'].apply(text_processor_model.preprocess)
        df['tokenized'] = df['preprocessed'].apply(lambda x: x.split())

        # Kirim DataFrame yang telah diproses kembali sebagai JSON
        return jsonify(df.to_dict(orient='records'))
    else:
        return jsonify({'error': 'Invalid file'}), 400

if __name__ == '__main__':
    app.run(debug=True)
