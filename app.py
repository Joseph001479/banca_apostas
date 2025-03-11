from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
from dotenv import load_dotenv
import os
from waitress import serve  # Importando o Waitress

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__, template_folder='.')  # Configura a raiz como pasta de templates
CORS(app)  # Habilitar comunicação com o frontend

# Configuração de segurança
app.secret_key = os.getenv('FLASK_SECRET_KEY')  # Usando a chave secreta do .env
app.permanent_session_lifetime = timedelta(minutes=30)  # Sessão expira após 30 minutos

# Pegar a URL de conexão do banco de dados do Heroku (PostgreSQL) do .env
DATABASE_URL = os.getenv('DATABASE_URL')

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desabilitar o tracking de modificações

db = SQLAlchemy(app)

# Definir o modelo de Usuário
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # A senha será armazenada como hash

# Criar tabelas no banco (quando necessário)
with app.app_context():
    db.create_all()

# Rota para a URL raiz
@app.route('/')
def home():
    return render_template('index.html')  # Aqui você renderiza a página de login

# Rota de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            dados = request.get_json()
            if not dados or 'username' not in dados or 'password' not in dados:
                return jsonify({'success': False, 'message': 'Campos obrigatórios ausentes'}), 400

            usuario = Usuario.query.filter_by(username=dados['username']).first()

            if usuario and check_password_hash(usuario.password, dados['password']):
                session.permanent = True  # A sessão será mantida por 30 minutos
                session['username'] = usuario.username  # Armazenando o nome de usuário na sessão
                return jsonify({'success': True, 'message': 'Login bem-sucedido!'}), 200  # Resposta de sucesso
            else:
                return jsonify({'success': False, 'message': 'Credenciais inválidas!'}), 401
        except Exception as e:
            return jsonify({'success': False, 'message': f'Erro no login: {str(e)}'}), 500

    return render_template('index.html')  # Retorna para o login se for GET

# Rota do dashboard
@app.route('/dash.html')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('home'))  # Redireciona para a página de login se não estiver autenticado
    return render_template('dash.html')

# Rota de cadastro
@app.route('/register', methods=['POST'])
def register():
    try:
        dados = request.get_json()
        if not dados or 'username' not in dados or 'password' not in dados or 'confirm_password' not in dados:
            return jsonify({'success': False, 'message': 'Por favor, preencha todos os campos!'}), 400

        if dados['password'] != dados['confirm_password']:
            return jsonify({'success': False, 'message': 'As senhas não coincidem!'}), 400

        usuario_existente = Usuario.query.filter_by(username=dados['username']).first()
        if usuario_existente:
            return jsonify({'success': False, 'message': 'Usuário já existe!'}), 409  # Conflito - Usuário existente

        # Gerar hash da senha
        hashed_password = generate_password_hash(dados['password'], method='pbkdf2:sha256')
        novo_usuario = Usuario(username=dados['username'], password=hashed_password)
        db.session.add(novo_usuario)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Cadastro realizado com sucesso!'}), 201  # Criado
    except Exception as e:
        return jsonify({'success': False, 'message': f'Erro no cadastro: {str(e)}'}), 500

# Rota de logout
@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove o usuário da sessão
    return redirect(url_for('home'))  # Redireciona para a página de login

# Usando o Waitress para produção
if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000) 
