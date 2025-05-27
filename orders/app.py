from flask import Flask, jsonify
import redis
import requests
import mysql.connector
import os
import time

# Inicializa o Flask
app = Flask(__name__)

# Conecta ao Redis (cache)
cache = redis.Redis(host=os.environ.get('REDIS_HOST', 'redis'), port=6379)

@app.route('/order')
def criar_pedido():
    # Tenta pegar produto do cache do Redis
    produto_cache = cache.get('produto_em_cache')
    if produto_cache:
        produto = eval(produto_cache)
        print("Produto encontrado no cache:", produto)
    else:
        print("Produto não estava em cache, buscando na API de produtos...")
        resposta = requests.get('http://products:3001/products')
        produto = resposta.json()['products'][0]
        cache.set('produto_em_cache', str(produto))
        print("Produto salvo em cache:", produto)

    # Conecta ao MySQL
    try:
        db = mysql.connector.connect(
            host=os.environ.get("DB_HOST", "db"),
            user=os.environ.get("DB_USER", "root"),
            password=os.environ.get("DB_PASSWORD", "example"),
            database=os.environ.get("DB_NAME", "ecommerce")
        )
        cursor = db.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS pedidos (id INT AUTO_INCREMENT PRIMARY KEY, produto_id INT, quantidade INT, valor_total INT)"
        )
        cursor.execute(
            "INSERT INTO pedidos (produto_id, quantidade, valor_total) VALUES (%s, %s, %s)",
            (produto['id'], 2, produto['price'] * 2)
        )
        db.commit()
        print(f"Pedido registrado no banco para produto id {produto['id']}")
    except Exception as erro:
        print("Erro ao salvar pedido no banco:", erro)
    finally:
        cursor.close()
        db.close()

    return jsonify({
        "codigo_pedido": 101,
        "produto_id": produto['id'],
        "quantidade": 2,
        "valor_total": produto['price'] * 2
    })

if __name__ == "__main__":
    # Tenta se conectar ao MySQL antes de subir a API
    print("Aguardando conexão com o banco de dados...")
    for tentativa in range(10):
        try:
            db = mysql.connector.connect(
                host=os.environ.get("DB_HOST", "db"),
                user=os.environ.get("DB_USER", "root"),
                password=os.environ.get("DB_PASSWORD", "example"),
                database=os.environ.get("DB_NAME", "ecommerce")
            )
            db.close()
            print("Banco conectado com sucesso!")
            break
        except Exception as e:
            print(f"Tentativa {tentativa + 1}: Banco ainda não disponível, aguardando...")
            time.sleep(2)
    print("Subindo servidor Flask na porta 3002")
    app.run(host='0.0.0.0', port=3002)
