from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS  # Importar CORS
from cone import obtener_clientes, obtener_productos, obtener_sucursales, insertar_compra, insertar_producto, obtener_todos_productos,insertar_cliente,obtener_compras, insertar_devolucion,insertar_sucursal,obtener_ubi_clientes,obtener_ubi_sucursales

app = Flask(__name__)

# Habilitar CORS para todas las rutas
CORS(app)

#Insertar comentarios
try:
    client = MongoClient("mongodb+srv://root:12345@entregafinal.ug2cb.mongodb.net/?retryWrites=true&w=majority&tls=true&tlsAllowInvalidCertificates=true")
    mongo_db = client["entregaFinal"]
    print("Conexión exitosa")
except Exception as e:
    print("Error en la conexión:", e)

comments_collection = mongo_db["Comentarios"]

# Ruta para insertar un comentario
@app.route("/insertar_comentarios", methods=["POST"])
def insertar_comentario():
    try:
        data = request.json
        print("Datos recibidos:", data)
        nuevo_comentario = {
            "customer_name": data["clienteId"],
            "productid": data["productoId"],
            "comment": data["comentario"],
            "rating": int(data["calificacion"])
        }
        comments_collection.insert_one(nuevo_comentario)
        print("Comentario insertado:", nuevo_comentario)
        return jsonify({"mensaje": "Comentario registrado exitosamente"}), 201
    except Exception as e:
        print("Error al insertar comentario:", e)
        return jsonify({"error": str(e)}), 500

    
# Ruta para obtener todos los comentarios
@app.route("/comentarios/todos", methods=["GET"])
def obtener_todos_comentarios():
    try:
        comentarios = list(comments_collection.find({}))
        for comentario in comentarios:
            comentario["_id"] = str(comentario["_id"])  # Convertir ObjectId a string
        return jsonify(comentarios), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#Ruta para obtener compras
@app.route("/obtener_compras", methods=["GET"])
def api_obtener_compras():
    try:
        sucursales = obtener_compras()  # Llamamos a la función que obtiene las compras
        return jsonify(sucursales), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
# Ruta para obtener clientes
@app.route("/obtener_clientes", methods=["GET"])
def api_obtener_clientes():
    try:
        clientes = obtener_clientes()  # Llamamos a la función que obtiene los clientes
        return jsonify(clientes), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta para obtener productos
@app.route("/obtener_productos", methods=["GET"])
def api_obtener_productos():
    try:
        productos = obtener_productos()  # Llamamos a la función que obtiene los productos
        return jsonify(productos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta para obtener sucursales
@app.route("/obtener_sucursales", methods=["GET"])
def api_obtener_sucursales():
    try:
        sucursales = obtener_sucursales()  # Llamamos a la función que obtiene las sucursales
        return jsonify(sucursales), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta para insertar una compra
@app.route("/insertar_compra", methods=["POST"])
def api_insertar_compra():
    try:
        data = request.json
        compra_id = data["compraId"]
        cliente_id = data["clienteId"]
        producto_id = data["productoId"]
        sucursal_id = data["sucursalId"]
        
        insertar_compra(compra_id, cliente_id, producto_id, sucursal_id)
        return jsonify({"message": "Compra registrada exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/insertar_producto", methods=["POST"])
def api_insertar_producto():
    try:
        data = request.json
        producto_id = data["productoId"]
        nombre = data["nombre"]
        descripcion = data["descripcion"]
        precio = data["precio"]
        stock = data["stock"]
        
        insertar_producto(producto_id, nombre, descripcion, precio, stock)
        return jsonify({"message": "Registrado exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/obtener_todos_productos", methods=["GET"])
def api_obtener_todos_productos():
    try:
        productos = obtener_todos_productos()  # Llamamos a la función que obtiene los clientes
        return jsonify(productos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/insertar_cliente", methods=["POST"])
def api_insertar_cliente():
    try:
        data = request.json
        cliente_id = data["clienteId"]
        nombre = data["nombre"]
        correo = data["correo"]
        latitud = data["latitud"]
        longitud = data["longitud"]
        
        insertar_cliente(cliente_id, nombre, correo, latitud, longitud)
        return jsonify({"message": "Registrado exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/insertar_devolucion", methods=["POST"])
def api_insertar_devolucion():
    try:
        data = request.json
        devolucion_id = data["devolucionId"]
        compra_id = data["compraId"]
        sucursal_id = data["sucursalId"]
        fecha_devolucion = data["fechaDevolucion"]
        motivo = data ["motivo"]
        
        insertar_devolucion(devolucion_id, compra_id, sucursal_id, fecha_devolucion, motivo)
        return jsonify({"message": "Devolucion registrada exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/insertar_sucursal", methods=["POST"])
def api_insertar_sucursal():
    try:
        data = request.json
        sucursal_id = data["sucursalId"]
        nombre = data["nombre"]
        latitud = data["latitud"]
        longitud = data["longitud"]
        
        insertar_sucursal(sucursal_id, nombre, latitud, longitud)
        return jsonify({"message": "Registrado exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta para obtener clientes y sucursales con sus ubicaciones
@app.route("/get_locations", methods=["GET"])
def get_locations():
    try:
        # Obtener los clientes
        clientes = obtener_ubi_clientes()  # Asegúrate de que esta función retorne una lista de clientes con latitud y longitud

        # Obtener las sucursales
        sucursales = obtener_ubi_sucursales()  # Asegúrate de que esta función retorne una lista de sucursales con latitud y longitud

        # Devuelve los clientes y sucursales como JSON
        return jsonify(clientes=clientes, sucursales=sucursales), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    



if __name__ == "__main__":
    app.run(debug=True)
