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

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    user = session.get('user')
    senha = session.get('senha')
    
    if (user != None or user != "" and senha != None or senha != "" and gerenciamentoUsers.containsUser(user)):
        if (gerenciamentoUsers.senhaCorreta(user, senha)):
            return redirect(url_for('dashboard'))
        
    if (request.method == 'POST'):
        formUser = request.form.get('user')
        formSenha = request.form.get('senha')
        
        if (gerenciamentoUsers.containsUser(formUser)):
            if (gerenciamentoUsers.senhaCorreta(formUser, formSenha)):
                session['user'] = formUser
                session['senha'] = formSenha
                return redirect(url_for('dashboard'))
        
        message = 'Usuário ou senha incorretos'
    
    return render_template('login.html', message = message)

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    message = ''
    user = session.get('user')
    senha = session.get('senha')
    
    if (user != None or user != "" and senha != None or senha != ""):
        if (gerenciamentoUsers.senhaCorreta(user, senha)):
            return redirect(url_for('dashboard'))
        
    if (request.method == 'POST'):
        formUser = str(request.form.get('user'))
        formSenha = str(request.form.get('senha'))
        formCSenha = str(request.form.get('cSenha'))
        
        if (gerenciamentoUsers.containsUser(formUser)):
            message = 'Usuário já cadastrado'
        else:
            if (formSenha == formCSenha):
                gerenciamentoUsers.criarUser(formUser, formSenha, 1)
                session['user'] = formUser
                session['senha'] = formSenha
                return redirect(url_for('dashboard'))
            else:
                message = 'Senhas não conferem.' + str(formCSenha) + ' / ' + str(formSenha)
    
    return render_template('registro.html', message = message)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    user = session.get('user')
    senha = session.get('senha')
    
    if (user != None or user != "" and senha != None or senha != ""):
        if (gerenciamentoUsers.senhaCorreta(user, senha)):
            return render_template('dashboard.html')
    
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('senha', None)
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    gerenciamentoUsers.criarTabela()
    
    app.run(host='127.0.0.1', port=8000, debug=True)