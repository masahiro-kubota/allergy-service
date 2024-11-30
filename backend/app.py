from flask import Flask, request, jsonify
from flask_cors import CORS
from flask.json import JSONEncoder
import json

class CustomJSONEcoder(JSONEncoder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ensure_ascii = False

app = Flask(__name__)
app.json_encoder = CustomJSONEcoder
CORS(app)

# メモリ内データベース（簡易版）
database = []

@app.route('/register', methods=['POST'])
def register_allergy():
    data = request.json
    if not data.get('allergy') or not data.get('severity'):
        return jsonify({"message": "アレルギー対象と重症度は必須です"}), 400

    database.append(data)  # データをメモリに保存
    return jsonify({"message": "アレルギー情報が登録されました"}), 201

@app.route('/info', methods=['GET'])
def get_all_allergies():
    return jsonify(database), 200

if __name__ == '__main__':
    app.run(debug=True)
