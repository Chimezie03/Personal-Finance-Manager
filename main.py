from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize the database
def init_db():
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS transactions 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, type TEXT, amount REAL)''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    total_income = 0
    total_expenses = 0
    transactions = []

    conn = sqlite3.connect('finance.db')
    c = conn.cursor()

    # Add transaction if POST request
    if request.method == 'POST':
        if 'clear' in request.form:
            # Clear all transactions
            c.execute("DELETE FROM transactions")
            conn.commit()
        else:
            t_type = request.form['type']
            amount = float(request.form['amount'])
            c.execute("INSERT INTO transactions (type, amount) VALUES (?, ?)", (t_type, amount))
            conn.commit()

    # Fetch all transactions
    c.execute("SELECT * FROM transactions")
    transactions = c.fetchall()

    # Calculate totals
    for t in transactions:
        if t[1] == 'income':
            total_income += t[2]
        elif t[1] == 'expense':
            total_expenses += t[2]

    conn.close()

    balance = total_income - total_expenses  # Subtract expenses from income
    return render_template('index.html', balance=balance, transactions=transactions)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
