from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Create DB table if not exists
def init_db():
    with sqlite3.connect('bills.db') as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS bills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT,
                item TEXT,
                quantity INTEGER,
                price REAL,
                total REAL
            )
        ''')
        conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-bill', methods=['POST'])
def generate_bill():
    customer_name = request.form['customer_name']
    item = request.form['item']
    quantity = int(request.form['quantity'])
    price = float(request.form['price'])
    total = quantity * price

    with sqlite3.connect('bills.db') as conn:
        c = conn.cursor()
        c.execute("INSERT INTO bills (customer_name, item, quantity, price, total) VALUES (?, ?, ?, ?, ?)",
                  (customer_name, item, quantity, price, total))
        conn.commit()

    return render_template('bill.html', name=customer_name, item=item, quantity=quantity, price=price, total=total)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
