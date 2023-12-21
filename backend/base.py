from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Izinkan semua domain (hati-hati di produksi)

@app.route("/profile", methods=["GET"])
def get_profile():
    # ... (logika untuk mendapatkan profil)
    return jsonify({"name": "John Doe", "about": "About messhshsh"})

if __name__ == "__main__":
    app.run(debug=True)
