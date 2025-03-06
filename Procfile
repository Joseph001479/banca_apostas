from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)  # Habilitar comunicação com o frontend

# Conectar ao banco de dados MySQL utilizando a URL fornecida
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://p1qexitu5ewqis3n:pqsv3y2uzvdbx68u@nwhazdrp7hdpd4a4.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/go0mmxvr550d0bbl'
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
    dados = request.json
    usuario = Usuario.query.filter_by(username=dados['username']).first()

    if usuario and check_password_hash(usuario.password, dados['password']):
        return jsonify({'success': True, 'message': 'Login bem-sucedido!'})
    else:
        return jsonify({'success': False, 'message': 'Credenciais inválidas!'})

# Rota de cadastro
@app.route('/register', methods=['POST'])
def register():
    dados = request.json
    usuario_existente = Usuario.query.filter_by(username=dados['username']).first()

    if usuario_existente:
        return jsonify({'success': False, 'message': 'Usuário já existe!'})

    # Gerar hash da senha com o método correto
    hashed_password = generate_password_hash(dados['password'], method='pbkdf2:sha256')
    novo_usuario = Usuario(username=dados['username'], password=hashed_password)
    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Cadastro realizado com sucesso!'})

if __name__ == '__main__':
    app.run(debug=True, port=5001)

