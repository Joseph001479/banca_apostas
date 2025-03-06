import mysql.connector

# Configuração do banco de dados no Heroku (use os dados do JAWSDB)
db_config = {
    "host": "nwhazdrp7hdpd4a4.cbetxkdyhwsb.us-east-1.rds.amazonaws.com",
    "user": "p1qexitu5ewqis3n",
    "password": "pqsv3y2uzvdbx68u",
    "database": "go0mmxvr550d0bbl"
}

try:
    conn = mysql.connector.connect(**db_config)
    if conn.is_connected():
        print("✅ Conexão bem-sucedida com o MySQL no Heroku!")
        conn.close()
except mysql.connector.Error as err:
    print(f"❌ Erro ao conectar: {err}")
