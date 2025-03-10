import os

class Config:
    # Chave secreta para segurança do Flask
    SECRET_KEY = '647594aa7013904964f9a4cb79cbbf1e107d0d3596175d34bda8d8a72a347103'

    # URL de conexão com o banco de dados PostgreSQL no Heroku
    SQLALCHEMY_DATABASE_URI = 'postgresql://u1qic7c7r61lgb:pf89ff5c7efa46e7f8652edf5e2c75dcf683eb6b15bd3446b3538f0f062364725@c3cj4hehegopde.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d6eva15k019f5u'

    # Para evitar avisos do SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
