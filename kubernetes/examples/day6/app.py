from flask import Flask, request, render_template, redirect, url_for
import psycopg2
import os

app = Flask(__name__)

DB_HOST = os.environ['DB_HOST']
DB_NAME = os.environ['DB_NAME']
DB_USER = os.environ['DB_USER']
DB_PASS = os.environ['DB_PASS']

def get_db_connection():
    return psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('form'))
    return render_template('login.html')

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        role = request.form['role']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO employees (name, email, role) VALUES (%s, %s, %s)", (name, email, role))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('list_employees'))
    return render_template('form.html')

@app.route('/list')
def list_employees():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM employees")
    employees = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('list.html', employees=employees)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

