import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from waitress import serve  # Importando o Waitress

app = Flask(__name__)
CORS(app)  # Habilitar comunicação com o frontend

# Pegar a URL de conexão do banco de dados do Heroku (PostgreSQL)
DATABASE_URL = os.getenv('DATABASE_URL')

# Ajuste a string de conexão para o PostgreSQL
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://")

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

# Desabilitar o tracking de modificações, recomendado no Flask
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Definir o modelo de Usuário
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # A senha será armazenada como hash

# Criar tabelas no banco (quando necessário)
with app.app_context():
    db.create_all()

# Rota de login
@app.route('/login', methods=['POST'])
def login():
    try:
        dados = request.json
        usuario = Usuario.query.filter_by(username=dados['username']).first()

        if usuario and check_password_hash(usuario.password, dados['password']):
            return jsonify({'success': True, 'message': 'Login bem-sucedido!'})
        else:
            return jsonify({'success': False, 'message': 'Credenciais inválidas!'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Erro no login: {str(e)}'})

# Rota de cadastro
@app.route('/register', methods=['POST'])
def register():
    try:
        dados = request.json
        # Verificar se as senhas coincidem
        if dados['password'] != dados['confirm_password']:
            return jsonify({'success': False, 'message': 'As senhas não coincidem!'})

        usuario_existente = Usuario.query.filter_by(username=dados['username']).first()

        if usuario_existente:
            return jsonify({'success': False, 'message': 'Usuário já existe!'})

        # Gerar hash da senha com o método correto
        hashed_password = generate_password_hash(dados['password'], method='pbkdf2:sha256')
        novo_usuario = Usuario(username=dados['username'], password=hashed_password)
        db.session.add(novo_usuario)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Cadastro realizado com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Erro no cadastro: {str(e)}'})

# Usando o Waitress para produção
if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5001)  # Rodando o servidor na porta 5001