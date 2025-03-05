from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='J@se001479',
        database='gestao_banca'
    )

@app.route('/adicionar_aposta', methods=['POST'])
def adicionar_aposta():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dados inválidos'}), 400

    nome_time = data.get('nomeTime')
    valor_aposta = data.get('valorAposta')
    odds = data.get('odds')
    resultado = data.get('resultado')

    if not all([nome_time, valor_aposta, odds, resultado]):
        return jsonify({'error': 'Campos faltando'}), 400

    usuario_id = 1  # Exemplo de ID fixo

    # Conectar ao banco
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO apostas (id_usuario, nomeTime, valorAposta, odds, resultado) VALUES (%s, %s, %s, %s, %s)",
            (usuario_id, nome_time, valor_aposta, odds, resultado)
        )
        conn.commit()

        # Atualizar saldo
        novo_saldo = valor_aposta * odds if resultado == 'win' else -valor_aposta
        cursor.execute("UPDATE saldos SET saldo = saldo + %s WHERE id_usuario = %s", (novo_saldo, usuario_id))
        conn.commit()

        # Buscar saldo atualizado
        cursor.execute("SELECT saldo FROM saldos WHERE id_usuario = %s", (usuario_id,))
        saldo_atualizado = cursor.fetchone()[0]
        lucro = saldo_atualizado - 100
        roi = (lucro / valor_aposta) * 100 if valor_aposta > 0 else 0

        return jsonify({
            'success': True,
            'saldo': saldo_atualizado,
            'lucro': lucro,
            'roi': roi
        })
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    # Rodar na porta 5001
    app.run(debug=True, port=5001)
