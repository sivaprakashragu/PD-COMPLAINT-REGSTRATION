from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)

# MySQL Connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",          # your MySQL username
        password="Sp@17102005",  # your MySQL password
        database="complaint_db"
    )


@app.route('/')
def home():
    return render_template('complaint.html')


@app.route('/add', methods=['POST'])
def add_complaint():
    name = request.form['name']
    email = request.form['email']
    contact = request.form['contact']
    ctype = request.form['type']
    description = request.form['description']

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO complaints (name, email, contact, type, description)
        VALUES (%s, %s, %s, %s, %s)
    """
    values = (name, email, contact, ctype, description)

    cursor.execute(query, values)
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('view_complaints'))


@app.route('/view')
def view_complaints():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM complaints")
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('view.html', complaints=data)


@app.route('/delete/<int:id>')
def delete(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM complaints WHERE id=%s", (id,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('view_complaints'))

@app.route('/edit/<int:id>')
def edit(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM complaints WHERE id=%s", (id,))
    complaint = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template('edit.html', complaint=complaint)

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    name = request.form['name']
    email = request.form['email']
    contact = request.form['contact']
    ctype = request.form['type']
    description = request.form['description']

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        UPDATE complaints
        SET name=%s, email=%s, contact=%s, type=%s, description=%s
        WHERE id=%s
    """
    values = (name, email, contact, ctype, description, id)

    cursor.execute(query, values)
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('view_complaints'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            session['user_id'] = user[0]
            return redirect(url_for('home'))
        else:
            return "Invalid credentials"

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for('login'))

    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)
