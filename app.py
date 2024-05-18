from flask import Flask, render_template, url_for, make_response
from flask_cors import CORS
from dotenv import load_dotenv
import os
import secrets

load_dotenv()

app = Flask(__name__)
app.config['secret_key'] = secrets.token_hex(64)
app.config['APP_TOKEN'] = secrets.token_hex(400)
CORS(app)

headers = {
    'Content-Type': 'text/html',
    'charset': 'utf-8',
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With",
    "Authorization": "Bearer " + app.config['APP_TOKEN']
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index2')
def index_2():
    return render_template('index_2.html')

@app.route('/index3')
def index_3():
    return render_template('index_3.html')

@app.route('/index4')
def index_4():
    return render_template('index_4.html')

@app.route('/index5')
def index_5():
    return render_template('index_5.html')

@app.route('/index6')
def index_6():
    return render_template('index_6.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/service')
def service():
    return render_template('service.html')

@app.route('/choose_us')
def choose_us():
    return render_template('choose_us.html')

@app.route('/testimonial')
def testimonial():
    return render_template('testimonial.html')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/login_register')
def login_register():
    return render_template('login_register.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/blog_standard')
def blog_standard():
    return render_template('blog_standard.html')

@app.route('/blog_details')
def blog_details():
    return render_template('blog_details.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.after_request
def add_headers(response):
    for key, value in headers.items():
        response.headers[key] = value
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
