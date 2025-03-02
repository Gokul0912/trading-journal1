from flask import Flask, request, jsonify
import sqlite3
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "trading_journal.db")

# Create database
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

@app.route('/add_trade', methods=['POST'])
def add_trade():
    data = request.json
    ai_insight = f"Trade on {data['asset']} analyzed."

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO trades (date, asset, entry_price, exit_price, strategy, ai_insight)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (data['date'], data['asset'], data['entry_price'], data['exit_price'], data['strategy'], ai_insight))
    conn.commit()
    trade_id = c.lastrowid  # Get the inserted trade's ID
    conn.close()
    
    return jsonify({"message": "Trade added successfully!", "ai_insight": ai_insight, "trade_id": trade_id})

@app.route('/get_trades', methods=['GET'])
def get_trades():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, date, asset, entry_price, exit_price, strategy, ai_insight FROM trades")
    trades = [{"id": row[0], "date": row[1], "asset": row[2], "entry_price": row[3], "exit_price": row[4], "strategy": row[5], "ai_insight": row[6]} for row in c.fetchall()]
    conn.close()
    
    return jsonify(trades)

@app.route('/delete_trade/<int:trade_id>', methods=['DELETE'])
def delete_trade(trade_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM trades WHERE id = ?", (trade_id,))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Trade deleted successfully!", "trade_id": trade_id})

if __name__ == '__main__':
    create_table()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

