from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
from libs.db.dbAPI import GerenciamentoUsers

app = Flask(__name__, template_folder="../frontend/templates")

app.static_folder = '../frontend/src'
app.static_url_path = '/static'

app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

gerenciamentoUsers = GerenciamentoUsers()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/servicos')
def servicos():
    return render_template('servicos.html')

@app.route('/login')
def login():
    user = session.get('user')
    senha = session.get('senha')
    
    if (user != None or user != "" and senha != None or senha != ""):
        if (gerenciamentoUsers.senhaCorreta(user, senha)):
            return redirect(url_for('dashboard'))
    
    return render_template('login.html')

@app.route('/registro')
def registro():
    user = session.get('user')
    senha = session.get('senha')
    
    if (user != None or user != "" and senha != None or senha != ""):
        if (gerenciamentoUsers.senhaCorreta(user, senha)):
            return redirect(url_for('dashboard'))
    
    return render_template('registro.html')

@app.route('/dashboard')
def dashboard():
    user = session.get('user')
    senha = session.get('senha')
    
    if (user != None or user != "" and senha != None or senha != ""):
        if (gerenciamentoUsers.senhaCorreta(user, senha)):
            return render_template('dashboard.html')
    
    return redirect(url_for('login'))

if __name__ == '__main__':
    gerenciamentoUsers.criarTabela()
    
    app.run(host='127.0.0.1', port=8000, debug=True)