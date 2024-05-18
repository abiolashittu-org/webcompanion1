from flask import Flask, render_template, url_for, make_response, redirect, request, session
from flask_cors import CORS
from dotenv import load_dotenv
import os
import secrets
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from passlib.hash import sha256_crypt
import logging
from functools import wraps

logging.basicConfig(filename='flask_errors.log')

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['secret_key'] = secrets.token_hex(64)
app.config['APP_TOKEN'] = secrets.token_hex(400)
app.config['USER_TOKEN'] = secrets.token_hex(64)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ os.path.join(basedir, 'database.db')
CORS(app)
app.secret_key = secrets.token_hex(64)

db = SQLAlchemy(app)
headers = {
    # 'Content-Type': 'text/html',
    'charset': 'utf-8',
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With",
    # "Authorization": "Bearer " + app.config['APP_TOKEN']
}

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullName = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"{self.fullName}"

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session and session['logged_in'] and session['current_user']:
            print("User is logged in")
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap

@app.route('/')
def index_demo_1():
    session.pop('cookie', None)
    return render_template('index-demo-1.html')

@app.route('/index2')
def index_demo_2():
    return render_template('index-demo-2.html')

@app.route('/index3')
def index_demo_3():
    return render_template('index-demo-3.html')

@app.route('/discover')
def discover():
    return render_template('discover.html')

@app.route('/discover_2')
def discover_2():
    return render_template('discover-2.html')

# @app.route('/index6')
# def index_6():
#     return render_template('index_6.html')

@app.route('/discover_3')
def discover_3():
    return render_template('discover-3.html')

@app.route('/item_details')
@login_required
def item_details():
    return render_template('item-details.html')

@app.route('/on_sale')
def on_sale():
    return render_template('on-sale.html')

@app.route('/create_item')
@login_required
def create_item():
    return render_template('create-item.html')

@app.route('/shopping_cart')
def shopping_cart():
    return render_template('shopping-cart.html')

@app.route('/authors')
def authors():
    return render_template('authors.html')

@app.route('/profile')
@login_required
def profile():
    try:
        user = session['current_user']
        if 'logged_in' not in session:
            pass
        return render_template('profile.html', user=user)
    except Exception as e:
        print(e)
        return redirect(url_for('login'))

@app.route('/index_blog_with_sidebar')
def index_blog_with_sidebar():
    return render_template('index-blog-with-sidebar.html')

@app.route('/blog')
def index_blog():
    return render_template('index-blog.html')

@app.route('/index_single_blog')
def index_single_blog():
    return render_template('index-single-blog.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email').lower()
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user and sha256_crypt.verify(password, user.password):
            session['logged_in'] = True
            session['email'] = user.email
            session['id'] = user.id
            session['current_user'] = user.fullName
            session['cookie'] = app.config['USER_TOKEN']

            return redirect('profile')
        else:
            return redirect(request.referrer)
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    session.pop('email', None)
    session.pop('id', None)
    session.pop('current_user', None)
    session.pop('cookie', None)

    print("Logged out successfully")
    return redirect('login')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    try:
        if request.method == 'POST':
            name = request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')

            user = User(
                fullName=name,
                email = email,
                password = sha256_crypt.encrypt(password)
            )
            db.session.add(user)
            db.session.commit()

            logging.info("Successfully Registered")
            return redirect('login')
    except Exception as e:
        print(e)
        logging.error(e)
    return render_template('signup.html')

@app.route('/contact_us')
def contact_us():
    return render_template('contact-us.html')

@app.after_request
def add_headers(response):
    for key, value in headers.items():
        response.headers[key] = value
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
