from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask.json import JSONEncoder
import uuid

class CustomJSONEcoder(JSONEncoder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ensure_ascii = False

app = Flask(__name__)
app.json_encoder = CustomJSONEcoder
CORS(app)

# メモリ内データベース（簡易版）
database = {}

@app.route('/register', methods=['POST'])
def register_allergy():
    data = request.json
    if not data.get('allergy') or not data.get('severity'):
        return jsonify({"message": "アレルギー対象と重症度は必須です"}), 400
    unique_id = str(uuid.uuid4())
    database[unique_id] = data  # データをメモリに保存
    share_link = f"http://localhost:5000/share/{unique_id}"

    return jsonify({
        "message": "アレルギー情報が登録されました",
        "link": share_link
        }), 201

@app.route('/share/<string:unique_id>', methods=['GET'])
def get_allergy_info(unique_id):
    data = database.get(unique_id)
    if not data:
        return render_template('error.html', message="アレルギー情報が見つかりません"), 404
        #return jsonify({"message": "アレルギー情報が見つかりません"}), 404
    #return jsonify(data), 200
    return render_template('info.html', data=data)

@app.route('/info', methods=['GET'])
def get_all_allergies():
    return jsonify(database), 200

if __name__ == '__main__':
    app.run(debug=True)
