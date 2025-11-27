from flask import Flask, request, g, render_template, flash, session
import sqlite3
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import time
import threading

DATABASE = "database.db"
app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=app
)

app.secret_key = os.urandom(32).hex()
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True
FLAG = "NCW{fake_flag}"
admin_username = "tanknight_" + os.urandom(6).hex()
admin_password = FLAG
from sigma import *

@app.after_request
def after_request(response):
    response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self' https://cdn.tailwindcss.com/3.4.17 http://www.instagram.com/embed.js; style-src 'self' 'unsafe-inline'; frame-src https://www.instagram.com/;"
    return response

def get_db():
    """Return a DB connection for this request, creating it if needed."""
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE, timeout=30)
        g.db.row_factory = sqlite3.Row 
    return g.db

@app.route('/')
def home():
    username = session.get('username', 'Guest')
    if username == 'Guest':
        return "Hello " + username + "!" + '<script src="https://cdn.tailwindcss.com/3.4.17"></script><body class="min-h-screen flex flex-col items-center gap-4 justify-center bg-gradient-to-br from-slate-900 via-indigo-900 to-sky-900 text-slate-100 text-center font-sans"><br>Login untuk melihat easter egg.<a href="/login" class="px-6 py-3 bg-sky-500 hover:bg-sky-600 text-slate-900 font-semibold rounded-xl shadow-lg transition">Login</a></body>'
    else:
        return "Hello " + username + "!" + "<meta http-equiv='refresh' content='0; url=/dashboard' />"

@app.route('/dashboard')
def dashboard():
    if not session.get('user_id'):
        return "<meta http-equiv='refresh' content='0; url=/login' />" + "Please login first!"
    return '<script src="https://cdn.tailwindcss.com/3.4.17"></script><body class="min-h-screen flex items-center gap-4 justify-center bg-gradient-to-br from-slate-900 via-indigo-900 to-sky-900 text-slate-100 text-center font-sans">' + post_instagram_tersigma + post_instagram_tersigma_2 + '</body>' + f"<!-- flag gratis 👻: {FLAG[:5]} -->"

@app.route('/flag')
def flag():
    print(f"{session.get('username','Guest')} is trying to access /flag")
    if session.get('admin'):
        return FLAG
    return "kamu siapa bang?"

@app.route('/logout')
def logout():
    session.clear()
    return "<meta http-equiv='refresh' content='0; url=/login' />" + "Logout successful!"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('user_id'):
        return "<meta http-equiv='refresh' content='0; url=/' />" + "Already logged in!"
    
    if request.method == 'GET':
        return render_template('login.html')
    
    username = request.form['username']
    password = request.form['password']
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    db.close()
    
    if not user:
        return "<meta http-equiv='refresh' content='0; url=/login' />" + "Invalid credentials or account does not exists!"
    
    session['user_id'] = user['id']
    session['username'] = user['username']
    session['admin'] = user['admin']
    return "<meta http-equiv='refresh' content='0; url=/' />" + "Login successful!"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('user_id'):
        return "<meta http-equiv='refresh' content='0; url=/' />" + "Already logged in!"
    
    if request.method == 'GET':
        return render_template('register.html')
    
    username = request.form['username']
    password = request.form['password']
    
    db = get_db()
    cursor = db.cursor()
    try:
        if FLAG in password:
            cursor.execute('INSERT INTO users (username, password, admin) VALUES (?, ?, ?)', (username, password, True))
        else:
            cursor.execute('INSERT INTO users (username, password, admin) VALUES (?, ?, ?)', (username, password, False))
        db.commit()
        
        user_id = cursor.lastrowid
        cursor.execute('SELECT id, username, admin FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['admin'] = user['admin']
        message = "<meta http-equiv='refresh' content='0; url=/dashboard' />" + f"User {username} registered successfully."
    except sqlite3.IntegrityError:
        message = "<meta http-equiv='refresh' content='0; url=/register' />" +  f"User {username} already exists."
    finally:
        db.close()

    return message

def run_bot(url):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument("--ignore-certificate-errors")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-background-networking')
    options.add_argument('--disable-default-apps')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-sync')
    options.add_argument('--disable-translate')

    driver = webdriver.Chrome(options=options)
    try:
        ## STAGE 1: Registering admin account..
        driver.get("https://127.0.0.1:40111/register")
        driver.find_element(By.NAME, "username").send_keys(admin_username)
        driver.find_element(By.NAME, "password").send_keys(admin_password)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(1)
        try:
            ## STAGE 2: Login as admin..
            driver.get("https://127.0.0.1:40111/login")
            driver.find_element(By.NAME, "username").send_keys(admin_username)
            driver.find_element(By.NAME, "password").send_keys(admin_password)
            driver.find_element(By.XPATH, "//button[@type='submit']").click()
            time.sleep(1)
        except:
            ...
        ## STAGE 3: Visit the target URL
        print(f"Bot is visiting: {url}")
        print(driver.get_cookies())
        driver.get(url)
        time.sleep(10)
        print(driver.get_cookies())
        message = 'done.'
    except Exception as e:
        message = f"Error occurred: {e}"
        print(f"Error occurred: {e}")
    finally:
        driver.close()
    return message

@app.route('/report', methods=['GET', 'POST'])
@limiter.limit("5 per 10 minutes", methods=["POST"])
def report():
    if request.method == 'GET':
        return render_template('report.html')
    
    url = request.form['url']
    if not url.startswith("http://") and not url.startswith("https://"):
        return "Only http and https protocol allowed.", 400
    
    threading.Thread(target=run_bot, args=(url,)).start()
    return f"Report submitted! Our bot will visit url shortly."

def init_db():
    with app.app_context():
        db = get_db()
        cur = db.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                admin BOOLEAN NOT NULL DEFAULT 0
            )
            """
        )
        db.commit()
        
if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=40111, ssl_context='adhoc')