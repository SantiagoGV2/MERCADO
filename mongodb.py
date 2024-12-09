from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import mysql.connector
import decimal
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Configuración de MongoDB
mongo_uri = "mongodb+srv://root:12345@entregafinal.ug2cb.mongodb.net/?ssl=true&tlsAllowInvalidCertificates=true"
mongo_client = MongoClient(mongo_uri)
mongo_db = mongo_client["entregaFinal"]

# Configuración de MySQL
mysql_config = {
    "host": "localhost",
    "user": "root",
    "password": "12345",
    "database": "entrega"
}
mysql_conn = mysql.connector.connect(**mysql_config)
cursor = mysql_conn.cursor(dictionary=True)

# Función para convertir valores de tipo decimal a float
def convert_decimal_to_float(value):
    if isinstance(value, decimal.Decimal):
        return float(value)
    elif isinstance(value, dict):
        return {k: convert_decimal_to_float(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [convert_decimal_to_float(v) for v in value]
    return value

# Migración de datos desde MySQL a MongoDB
@app.route("/migrar", methods=["POST"])
def migrar_datos():
    try:
        # Migrar Clientes
        cursor.execute("SELECT * FROM Clientes")
        clientes = cursor.fetchall()
        mongo_db["Clientes"].insert_many(
            [{k: convert_decimal_to_float(v) for k, v in row.items()} for row in clientes]
        )

        # Migrar Productos
        cursor.execute("SELECT * FROM Productos")
        productos = cursor.fetchall()
        mongo_db["Productos"].insert_many(
            [{k: convert_decimal_to_float(v) for k, v in row.items()} for row in productos]
        )

        # Migrar Sucursales
        cursor.execute("SELECT * FROM Sucursales")
        sucursales = cursor.fetchall()
        mongo_db["Sucursales"].insert_many(
            [{k: convert_decimal_to_float(v) for k, v in row.items()} for row in sucursales]
        )

        # Migrar Compras con relaciones
        cursor.execute("SELECT * FROM Compras")
        compras = cursor.fetchall()
        for row in compras:
            row["Cliente"] = get_cliente(row.pop("cliente_id"))
            row["Producto"] = get_producto(row.pop("producto_id"))
            row["Sucursal"] = get_sucursal(row.pop("sucursal_id"))
            mongo_db["Compras"].insert_one({k: convert_decimal_to_float(v) for k, v in row.items()})

        # Migrar Devoluciones con relaciones
        cursor.execute("SELECT * FROM Devoluciones")
        devoluciones = cursor.fetchall()
        for row in devoluciones:
            row["Compra"] = get_compra(row.pop("compra_id"))
            row["Sucursal"] = get_sucursal(row.pop("sucursal_id"))
            mongo_db["Devoluciones"].insert_one({k: convert_decimal_to_float(v) for k, v in row.items()})

        return jsonify({"mensaje": "Migración completada"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Función para obtener datos relacionados
def get_cliente(cliente_id):
    cursor.execute("SELECT * FROM Clientes WHERE cliente_id = %s", (cliente_id,))
    return cursor.fetchone()

def get_producto(producto_id):
    cursor.execute("SELECT * FROM Productos WHERE producto_id = %s", (producto_id,))
    return cursor.fetchone()

def get_sucursal(sucursal_id):
    cursor.execute("SELECT * FROM Sucursales WHERE sucursal_id = %s", (sucursal_id,))
    return cursor.fetchone()

def get_compra(compra_id):
    cursor.execute("SELECT * FROM Compras WHERE compra_id = %s", (compra_id,))
    return cursor.fetchone()

@app.route("/comentarios", methods=["POST"])
def insertar_comentario():
    try:
        data = request.json
        comentario_doc = {
            "comentarioId": str(datetime.timestamp(datetime.now())),
            "productoId": data.get("productoId"),
            "clienteId": data.get("clienteId"),
            "comentario": data.get("comentario"),
            "calificacion": data.get("calificacion"),
            "fecha": datetime.now()
        }
        mongo_db.Comentarios.insert_one(comentario_doc)
        return jsonify({"mensaje": "Comentario insertado con éxito"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500




# Insertar calificación de un producto
@app.route("/productos", methods=["POST"])
def insertar_producto_calificado():
    data = request.json
    producto_doc = mongo_db.ProductosCalificados.find_one({"productoId": data["productoId"]})

    if producto_doc:
        mongo_db.ProductosCalificados.update_one(
            {"productoId": data["productoId"]},
            {"$push": {"calificaciones": {"clienteId": data["clienteId"], "calificacion": data["calificacion"]}}}
        )
    else:
        mongo_db.ProductosCalificados.insert_one({
            "productoId": data["productoId"],
            "calificaciones": [{"clienteId": data["clienteId"], "calificacion": data["calificacion"]}]
        })
    return jsonify({"mensaje": "Producto calificado con éxito"}), 201

# Consultar comentarios de un producto
@app.route("/comentarios/<productoId>", methods=["GET"])
def consultar_comentarios(productoId):
    comentarios = list(mongo_db.Comentarios.find({"productoId": productoId}, {"_id": 0}))
    return jsonify(comentarios), 200

# Consultar productos calificados
@app.route("/productos/calificados", methods=["GET"])
def consultar_productos():
    productos = list(mongo_db.ProductosCalificados.find({}, {"_id": 0}))
    return jsonify(productos), 200


@app.route("/productos", methods=["GET"])
def api_obtener_productos():
    try:
        cursor.execute("SELECT producto_id FROM Productos")
        productos = cursor.fetchall()
        # Devolver solo los ID de productos con un nombre estándar
        return jsonify([{"id": producto["producto_id"]} for producto in productos]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/clientes", methods=["GET"])
def api_obtener_clientes():
    try:
        cursor.execute("SELECT cliente_id FROM Clientes")
        clientes = cursor.fetchall()
        # Devolver solo los ID de clientes con un nombre estándar
        return jsonify([{"id": cliente["cliente_id"]} for cliente in clientes]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500





if __name__ == "__main__":
    app.run(debug=True)