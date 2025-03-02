from flask import Flask, request, jsonify
import sqlite3
import os
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Ensure database persistence on Render
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "trading_journal.db")

# Create database table
def create_table():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            asset TEXT,
            entry_price REAL,
            exit_price REAL,
            strategy TEXT,
            ai_insight TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return jsonify({"message": "Trading Journal API is Running!"})

# Run Flask app
if __name__ == '__main__':
    create_table()
    port = int(os.environ.get("PORT", 5000))  # Use Render’s PORT
    app.run(host='0.0.0.0', port=port, debug=True)

