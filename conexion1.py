from pymongo import MongoClient
import mysql.connector
import decimal

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

# Función para convertir valores de tipo decimal a float de forma recursiva
def convert_decimal_to_float(value):
    if isinstance(value, decimal.Decimal):
        return float(value)
    elif isinstance(value, dict):
        return {k: convert_decimal_to_float(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [convert_decimal_to_float(v) for v in value]
    return value

# Función para migrar la tabla 'Clientes'
def migrate_clientes():
    cursor.execute("SELECT * FROM Clientes")
    rows = cursor.fetchall()
    collection = mongo_db["Clientes"]
    for row in rows:
        # Convertimos todos los valores de decimal a float antes de insertar
        row = {k: convert_decimal_to_float(v) for k, v in row.items()}
        collection.insert_one(row)
    print("Migración de Clientes completada.")

# Función para migrar la tabla 'Productos'
def migrate_productos():
    cursor.execute("SELECT * FROM Productos")
    rows = cursor.fetchall()
    collection = mongo_db["Productos"]
    for row in rows:
        # Convertimos todos los valores de decimal a float antes de insertar
        row = {k: convert_decimal_to_float(v) for k, v in row.items()}
        collection.insert_one(row)
    print("Migración de Productos completada.")

# Función para migrar la tabla 'Sucursales'
def migrate_sucursales():
    cursor.execute("SELECT * FROM Sucursales")
    rows = cursor.fetchall()
    collection = mongo_db["Sucursales"]
    for row in rows:
        # Convertimos todos los valores de decimal a float antes de insertar
        row = {k: convert_decimal_to_float(v) for k, v in row.items()}
        collection.insert_one(row)
    print("Migración de Sucursales completada.")

# Función para migrar la tabla 'Compras' con relaciones
def migrate_compras():
    cursor.execute("SELECT * FROM Compras")
    rows = cursor.fetchall()
    collection = mongo_db["Compras"]
    for row in rows:
        # Se obtienen las relaciones y se asignan a los campos correspondientes
        row["Cliente"] = get_cliente(row.pop("cliente_id"))
        row["Producto"] = get_producto(row.pop("producto_id"))
        row["Sucursal"] = get_sucursal(row.pop("sucursal_id"))
        # Convertimos todos los valores de decimal a float antes de insertar
        row = {k: convert_decimal_to_float(v) for k, v in row.items()}
        collection.insert_one(row)
    print("Migración de Compras completada.")

# Función para migrar la tabla 'Devoluciones' con relaciones
def migrate_devoluciones():
    cursor.execute("SELECT * FROM Devoluciones")
    rows = cursor.fetchall()
    collection = mongo_db["Devoluciones"]
    for row in rows:
        # Se obtienen las relaciones y se asignan a los campos correspondientes
        row["Compra"] = get_compra(row.pop("compra_id"))
        row["Sucursal"] = get_sucursal(row.pop("sucursal_id"))
        # Convertimos todos los valores de decimal a float antes de insertar
        row = {k: convert_decimal_to_float(v) for k, v in row.items()}
        collection.insert_one(row)
    print("Migración de Devoluciones completada.")

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

# Función principal para migrar todas las tablas
def main():
    try:
        print("Iniciando migración...")
        migrate_clientes()
        migrate_productos()
        migrate_sucursales()
        migrate_compras()
        migrate_devoluciones()
        print("Migración completada.")
    except Exception as e:
        print(f"Error durante la migración: {e}")
    finally:
        mysql_conn.close()
        client.close()

# Ejecuta el proceso de migración
if __name__ == "__main__":
    main()
