from flask_sqlalchemy import SQLAlchemy

# Inicializar o SQLAlchemy para ser usado no app principal
db = SQLAlchemy()

# Criar a tabela 'Usuario'
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # ID único para cada usuário
    username = db.Column(db.String(100), unique=True, nullable=False)  # Nome de usuário único
    password = db.Column(db.String(200), nullable=False)  # Senha criptografada
