from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session

app = Flask(__name__, template_folder="../frontend/templates")

app.static_folder = '../frontend/src'
app.static_url_path = '/static'

app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    
    if request.method == 'POST':
        user = request.form.get('user')
        senha = request.form.get('senha')
        
    return render_template('index.html', message=message)