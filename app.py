from flask import Flask, render_template, request, redirect, session, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from config import DB_CONFIG

app = Flask(__name__)
app.secret_key = "secret_key_here"  # Use a strong secret key in production

# Connect to DB
def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

# Home Page
@app.route('/')
def index():
    return render_template('index.html')

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO students (name, email, password) VALUES (%s, %s, %s)",
                (name, email, hashed_password)
            )
            conn.commit()
            flash("Registration successful! Please login.", "success")
            return redirect('/login')
        except mysql.connector.Error as e:
            flash(f"Error: {e}", "danger")
            return render_template('register.html')
        finally:
            cursor.close()
            conn.close()
    return render_template('register.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM students WHERE email=%s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            flash(f"Welcome, {user['name']}!", "success")
            return redirect('/dashboard')
        else:
            flash("Invalid email or password", "danger")
            return render_template('login.html')

    return render_template('login.html')

# Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("Please login first.", "warning")
        return redirect('/login')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students WHERE id=%s", (session['user_id'],))
    user = cursor.fetchone()

    cursor.execute("SELECT * FROM notifications ORDER BY date_posted DESC")
    notifications = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('dashboard.html', notifications=notifications, user=user)

# Logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("Logged out successfully.", "info")
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
