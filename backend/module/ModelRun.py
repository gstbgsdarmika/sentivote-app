from flask import Flask, request, jsonify
from Preprocessing  import Preprocessing  

app = Flask(__name__)

# Create an instance of the Preprocessing class
preprocessor = Preprocessing()

@app.route('/analisis', methods=['POST'])
def preprocess_text():
    if request.method == 'POST':
        data = request.get_json()
        text_to_preprocess = data.get('text')

        if text_to_preprocess:
            preprocessed_text = preprocessor.preprocess_all(text_to_preprocess)
            return jsonify({"result": preprocessed_text})
        else:
            return jsonify({"error": "Missing 'text' parameter"}), 400
    else:
        return jsonify({"error": "Unsupported method"}), 405

if __name__ == '__main__':
    app.run(debug=True)
