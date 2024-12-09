from pymongo import MongoClient
import mysql.connector

# Establece la conexión con la base de datos MySQL
mysql_conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",
    database="entrega"
)
cursor = mysql_conn.cursor(dictionary=True)

# Establece la conexión con la base de datos MongoDB
client = MongoClient("mongodb+srv://root:12345@entregafinal.ug2cb.mongodb.net/")
mongo_db = client["entregaFinal"]

def insertar_compra(compra_id,cliente_id, producto_id, sucursal_id):
    try:
        # Inserta los datos en la tabla Compras
        query = """
        INSERT INTO Compras (compra_id, cliente_id, producto_id, sucursal_id)
        VALUES (%s,%s, %s, %s)
        """
        values = (compra_id, cliente_id, producto_id, sucursal_id)
        cursor.execute(query, values)
        mysql_conn.commit()
        print("Compra registrada exitosamente.")
    except Exception as e:
        print(f"Error al registrar la compra: {e}")

def insertar_devolucion(devolucion_id,compra_id,sucursal_id,fecha_devolucion,motivo):
    try:
        # Inserta los datos en la tabla Compras
        query = """
        INSERT INTO Devoluciones (devolucion_id, compra_id, sucursal_id, fecha_devolucion, motivo)
        VALUES (%s,%s, %s, %s, %s)
        """
        values = (devolucion_id, compra_id, sucursal_id, fecha_devolucion, motivo)
        cursor.execute(query, values)
        mysql_conn.commit()
        print("Devolucion registrada exitosamente.")
    except Exception as e:
        print(f"Error al registrar la devolucion: {e}")

def insertar_cliente(cliente_id,nombre,correo,latitud,longitud):
    try:
        # Inserta los datos en la tabla Compras
        query = """
        INSERT INTO Clientes (cliente_id, nombre, correo, latitud, longitud)
        VALUES (%s,%s, %s, %s, %s)
        """
        values = (cliente_id, nombre, correo, latitud, longitud)
        cursor.execute(query, values)
        mysql_conn.commit()
        print("Cliente registrada exitosamente.")
    except Exception as e:
        print(f"Error al registrar el cliente: {e}")

def insertar_sucursal(sucursal_id,nombre,latitud,longitud):
    try:
        # Inserta los datos en la tabla Compras
        query = """
        INSERT INTO Sucursales (sucursal_id, nombre, latitud, longitud)
        VALUES (%s,%s, %s, %s)
        """
        values = (sucursal_id, nombre, latitud, longitud)
        cursor.execute(query, values)
        mysql_conn.commit()
        print("Sucursal registrada exitosamente.")
    except Exception as e:
        print(f"Error al registrar la sucursal: {e}")

def insertar_producto(producto_id,nombre,descripcion,precio,stock):
    try:
        # Inserta los datos en la tabla Productos
        query = """
        INSERT INTO Productos (producto_id, nombre, descripcion, precio, stock)
        VALUES (%s,%s, %s, %s,%s)
        """
        values = (producto_id, nombre, descripcion, precio, stock)
        cursor.execute(query, values)
        mysql_conn.commit()
        print("Producto registrada exitosamente.")
    except Exception as e:
        print(f"Error al registrar el producto: {e}")



# Función para obtener los clientes desde la base de datos (id y nombre)
def obtener_clientes():
    cursor.execute("SELECT cliente_id, nombre FROM Clientes")
    rows = cursor.fetchall()
    return [{"id": row["cliente_id"], "nombre": row["nombre"]} for row in rows]

# Función para obtener los productos desde la base de datos (id y nombre)
def obtener_productos():
    cursor.execute("SELECT producto_id, nombre FROM Productos")
    rows = cursor.fetchall()
    return [{"id": row["producto_id"], "nombre": row["nombre"]} for row in rows]

def obtener_todos_productos():
    cursor.execute("SELECT nombre, descripcion, precio, stock FROM Productos")
    rows = cursor.fetchall()
    return [{"nombre": row["nombre"], "descripcion": row["descripcion"], "precio": row["precio"], "stock": row["stock"]} for row in rows]

# Función para obtener las sucursales desde la base de datos (id y nombre)
def obtener_sucursales():
    cursor.execute("SELECT sucursal_id, nombre FROM Sucursales")
    rows = cursor.fetchall()
    return [{"id": row["sucursal_id"], "nombre": row["nombre"]} for row in rows]


def obtener_compras():
    cursor.execute("SELECT compra_id FROM Compras")
    rows = cursor.fetchall()
    return [{"id": row["compra_id"]} for row in rows]

def obtener_ubi_clientes():
    cursor.execute("SELECT latitud, longitud FROM Clientes")
    rows = cursor.fetchall()
    for row in rows:
        print(f"Cliente - Latitud: {row['latitud']}, Longitud: {row['longitud']}")
    return [{"latitud": row["latitud"], "longitud": row["longitud"]} for row in rows]

def obtener_ubi_sucursales():
    cursor.execute("SELECT latitud, longitud FROM Sucursales")
    rows = cursor.fetchall()
    for row in rows:
        print(f"Sucursal - Latitud: {row['latitud']}, Longitud: {row['longitud']}")
    return [{"latitud": row["latitud"], "longitud": row["longitud"]} for row in rows]