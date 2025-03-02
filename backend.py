from flask import Flask, request, jsonify
import sqlite3
import os
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)

DB_NAME = os.path.join(os.getcwd(), "trading_journal.db")  # Database file path

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
            trade_type TEXT,  -- Buy or Sell
            profit_loss REAL,  -- Store calculated profit/loss
            strategy TEXT,
            ai_insight TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/add_trade', methods=['POST'])
def add_trade():
    data = request.json
    date = data['date']
    asset = data['asset']
    entry_price = float(data['entry_price'])
    exit_price = float(data['exit_price'])
    trade_type = data.get('trade_type', 'Buy')  # Default to "Buy" if not specified
    strategy = data['strategy']
    
    # Calculate Profit/Loss
    if trade_type.lower() == 'buy':
        profit_loss = exit_price - entry_price  # Long trade calculation
    elif trade_type.lower() == 'sell':
        profit_loss = entry_price - exit_price  # Short selling calculation
    else:
        profit_loss = 0  # Undefined trade type
    
    ai_insight = f"Trade on {asset} analyzed."

    # Insert into database
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO trades (date, asset, entry_price, exit_price, trade_type, profit_loss, strategy, ai_insight)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (date, asset, entry_price, exit_price, trade_type, profit_loss, strategy, ai_insight))
    
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Trade added successfully!", "profit_loss": profit_loss, "ai_insight": ai_insight})

@app.route('/get_trades', methods=['GET'])
def get_trades():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM trades")
    trades = c.fetchall()
    conn.close()

    trade_list = []
    for trade in trades:
        trade_list.append({
            "id": trade[0],
            "date": trade[1],
            "asset": trade[2],
            "entry_price": trade[3],
            "exit_price": trade[4],
            "trade_type": trade[5],
            "profit_loss": trade[6],
            "strategy": trade[7],
            "ai_insight": trade[8]
        })
    
    return jsonify(trade_list)

@app.route('/delete_trade/<int:trade_id>', methods=['DELETE'])
def delete_trade(trade_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM trades WHERE id = ?", (trade_id,))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Trade deleted successfully!"})

# Run Flask app
if __name__ == '__main__':
    create_table()
    app.run(host='0.0.0.0', port=5000, debug=True)

