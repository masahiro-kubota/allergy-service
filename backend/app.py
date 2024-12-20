#! /usr/bin/env python

from json import JSONEncoder
import os
import sqlite3
import uuid

from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

# TODO ファイルの分割
class CustomJSONEcoder(JSONEncoder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ensure_ascii = False


def init_db(DATABASE):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS allergies (
            id TEXT PRIMARY KEY,
            name TEXT,
            allergy TEXT NOT NULL,
            severity TEXT NOT NULL,
            treatment TEXT
        )
    ''')
    conn.commit()
    print("データベースが初期化されました")



def create_app():
    """Flaskアプリケーションを作成するファクトリ関数"""
    app = Flask(__name__)
    app.json_encoder = CustomJSONEcoder
    CORS(app)
    init_db("data/allergies.db")

    base_url = os.getenv("BASE_URL", "http://127.0.0.1:8000")
    

    @app.route('/register', methods=['POST'])
    def register_allergy():
        data = request.json
        if not data.get('allergy') or not data.get('severity'):
            return jsonify({"message": "アレルギー対象と重症度は必須です"}), 400
        unique_id = str(uuid.uuid4())
        #TODO "with as openと単純なconnectの違い。単純にconnectだと開けなくなる。同時にファイルをopenすることになるからか？"
        with sqlite3.connect("data/allergies.db") as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO allergies (id, name, allergy, severity, treatment)
                VALUES (?, ?, ?, ?, ?)
            ''', (unique_id, data.get('name'), data.get('allergy'), data.get('severity'), data.get('treatment')))
            conn.commit()
        print(base_url)
        share_link = f"{base_url}/share/{unique_id}"

        return jsonify({
            "message": "アレルギー情報が登録されました",
            "link": share_link
            }), 201

    @app.route('/share/<string:unique_id>', methods=['GET'])
    def get_allergy_info(unique_id):
        with sqlite3.connect("data/allergies.db") as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT name, allergy, severity, treatment FROM allergies WHERE id = ?
            ''', (unique_id,))
            row = cursor.fetchone()

        if not row:
            return render_template('error.html', message="アレルギー情報が見つかりません"), 404
        data = {
            "name": row[0],
            "allergy": row[1],
            "severity": row[2],
            "treatment": row[3]
        }
        response = render_template('info.html', data=data)
        return response

    @app.route('/info', methods=['GET'])
    def get_all_allergies():
        with sqlite3.connect("data/allergies.db") as conn:
            cursor = conn.cursor()
            # クエリを実行してデータを取得
            cursor.execute('SELECT id, name, allergy, severity, treatment FROM allergies')
            rows = cursor.fetchall()
        data = [
            {"id": row[0], "name": row[1], "allergy": row[2], "severity": row[3], "treatment": row[4]}
            for row in rows
        ]
        return jsonify(data), 200
    
    @app.route('/table', methods=['GET'])
    def show_table():
        # データベースからデータを取得
        with sqlite3.connect("data/allergies.db") as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, name, allergy, severity, treatment FROM allergies')
            rows = cursor.fetchall()
        
        # データを辞書形式に変換
        data = [
            {"id": row[0], "name": row[1], "allergy": row[2], "severity": row[3], "treatment": row[4]}
            for row in rows
        ]

        # テーブルを表示するHTMLをレンダリング
        return render_template('table.html', data=data)
    
    return app


load_dotenv()
# アプリケーションインスタンスを生成
app = create_app()
