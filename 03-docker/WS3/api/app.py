import os
import psycopg
from psycopg.rows import dict_row
from flask import Flask, jsonify, request

app = Flask(__name__)

# Variables de entorno
INSTANCE = os.environ.get("INSTANCE", "unknown")
DB_HOST = os.environ.get("DB_HOST", "db")
DB_NAME = os.environ.get("DB_NAME", "shop")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "postgres")

def get_db_connection():
    return psycopg.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        row_factory=dict_row
    )

@app.route('/products', methods=['GET'])
def get_products():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM products')
            products = cur.fetchall()
    return jsonify({"served_by": INSTANCE, "products": products})

@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM products WHERE id = %s', (id,))
            product = cur.fetchone()
    return jsonify({"served_by": INSTANCE, "product": product})

@app.route('/products', methods=['POST'])
def create_product():
    data = request.json
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('INSERT INTO products (name, price) VALUES (%s, %s) RETURNING *', 
                        (data['name'], data['price']))
            new_product = cur.fetchone()
            conn.commit()
    return jsonify({"served_by": INSTANCE, "product": new_product}), 201

@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.json
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('UPDATE products SET name = %s, price = %s WHERE id = %s RETURNING *', 
                        (data['name'], data['price'], id))
            updated = cur.fetchone()
            conn.commit()
    return jsonify({"served_by": INSTANCE, "product": updated})

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('DELETE FROM products WHERE id = %s', (id,))
            conn.commit()
    return jsonify({"served_by": INSTANCE, "message": "Deleted"})