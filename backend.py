from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow frontend to communicate with backend

DB_NAME = "trading_journal.db"

# Function to create database table
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

# Route to add a trade
@app.route('/add_trade', methods=['POST'])
def add_trade():
    try:
        data = request.json
        date = data.get("date")
        asset = data.get("asset")
        entry_price = float(data.get("entry_price"))
        exit_price = float(data.get("exit_price"))
        strategy = data.get("strategy")

        # Simple AI-generated insight
        profit_loss = exit_price - entry_price
        ai_insight = f"{'Good trade!' if profit_loss > 0 else 'Risky trade!'} You {'gained' if profit_loss > 0 else 'lost'} {abs(profit_loss)} units."

        # Insert trade into the database
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''
            INSERT INTO trades (date, asset, entry_price, exit_price, strategy, ai_insight)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (date, asset, entry_price, exit_price, strategy, ai_insight))
        conn.commit()
        conn.close()

        print("✅ Trade successfully inserted into the database!")
        return jsonify({"message": "Trade added successfully!", "ai_insight": ai_insight})

    except Exception as e:
        print("❌ Error inserting trade:", str(e))
        return jsonify({"error": "Failed to add trade"}), 500

# Route to fetch all trades
@app.route('/get_trades', methods=['GET'])
def get_trades():
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT date, asset, entry_price, exit_price, strategy, ai_insight FROM trades")
        trades = [
            {"date": row[0], "asset": row[1], "entry_price": row[2], "exit_price": row[3], "strategy": row[4], "ai_insight": row[5]}
            for row in c.fetchall()
        ]
        conn.close()
        return jsonify(trades)

    except Exception as e:
        print("❌ Error fetching trades:", str(e))
        return jsonify({"error": "Failed to retrieve trades"}), 500

# Route to delete all trades (Optional)
@app.route('/delete_trades', methods=['DELETE'])
def delete_trades():
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("DELETE FROM trades")
        conn.commit()
        conn.close()
        print("✅ All trades deleted successfully!")
        return jsonify({"message": "All trades deleted successfully!"})

    except Exception as e:
        print("❌ Error deleting trades:", str(e))
        return jsonify({"error": "Failed to delete trades"}), 500

# Run Flask app
if __name__ == '__main__':
    create_table()
    print("🚀 Backend is running on http://127.0.0.1:5000")
    app.run(debug=True)
