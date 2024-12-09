from pymongo import MongoClient
from datetime import datetime

# Configuración de la conexión
uri = "mongodb+srv://root:12345@entregafinal.ug2cb.mongodb.net/"

# Conexión a MongoDB
def conectar():
    try:
        client = MongoClient(uri)
        db = client['entregaFinal']  # Nombre de la base de datos
        print("Conexión exitosa a MongoDB")
        return db
    except Exception as e:
        print("Error conectando a MongoDB:", e)

# Crear colecciones
def crear_colecciones():
    db = conectar()
    # Crear colecciones
    db.create_collection("Comentarios")
    db.create_collection("ProductosCalificados")
    print("Colecciones creadas")

# Insertar un comentario
def insertar_comentario(productoId, clienteId, comentario, calificacion):
    db = conectar()
    comentario_doc = {
        "comentarioId": str(datetime.timestamp(datetime.now())),  # ID único con timestamp
        "productoId": productoId,
        "clienteId": clienteId,
        "comentario": comentario,
        "calificacion": calificacion,
        "fecha": datetime.now()
    }
    db.Comentarios.insert_one(comentario_doc)
    print(f"Comentario para el producto {productoId} insertado")

# Insertar un producto calificado
def insertar_producto_calificado(productoId, clienteId, calificacion):
    db = conectar()
    producto_doc = db.ProductosCalificados.find_one({"productoId": productoId})

    if producto_doc:
        db.ProductosCalificados.update_one(
            {"productoId": productoId},
            {"$push": {"calificaciones": {"clienteId": clienteId, "calificacion": calificacion}}}
        )
    else:
        db.ProductosCalificados.insert_one({
            "productoId": productoId,
            "calificaciones": [{"clienteId": clienteId, "calificacion": calificacion}]
        })
    print(f"Producto {productoId} calificado con {calificacion}")

# Consultar comentarios de un producto
def consultar_comentarios(productoId):
    db = conectar()
    comentarios = db.Comentarios.find({"productoId": productoId})
    for comentario in comentarios:
        print(f"Comentario: {comentario['comentario']}, Calificación: {comentario['calificacion']}")

# Calcular la calificación promedio de un producto
def calificacion_promedio(productoId):
    db = conectar()
    comentarios = db.Comentarios.find({"productoId": productoId})
    total_calificaciones = 0
    num_comentarios = 0

    for comentario in comentarios:
        total_calificaciones += comentario['calificacion']
        num_comentarios += 1

    if num_comentarios > 0:
        promedio = total_calificaciones / num_comentarios
        print(f"Calificación promedio del producto {productoId}: {promedio}")
    else:
        print(f"No hay comentarios para el producto {productoId}")

# Actualizar un comentario
def actualizar_comentario(comentarioId, nuevo_comentario):
    db = conectar()
    result = db.Comentarios.update_one(
        {"comentarioId": comentarioId},
        {"$set": {"comentario": nuevo_comentario}}
    )
    if result.modified_count > 0:
        print(f"Comentario {comentarioId} actualizado")
    else:
        print(f"No se encontró el comentario con ID {comentarioId}")

# Eliminar un comentario
def eliminar_comentario(comentarioId):
    db = conectar()
    result = db.Comentarios.delete_one({"comentarioId": comentarioId})
    if result.deleted_count > 0:
        print(f"Comentario {comentarioId} eliminado")
    else:
        print(f"No se encontró el comentario con ID {comentarioId}")

# Función principal para probar
def main():
    # Crear colecciones (Solo necesario la primera vez)
    # crear_colecciones()

    # Insertar comentarios
    insertar_comentario("123", "456", "Producto excelente", 5)
    insertar_comentario("123", "789", "Muy bueno, pero un poco caro", 4)

    # Insertar calificaciones para productos
    insertar_producto_calificado("123", "456", 5)
    insertar_producto_calificado("123", "789", 4)

    # Consultar comentarios de un producto
    print("Comentarios del producto 123:")
    consultar_comentarios("123")

    # Calcular calificación promedio
    calificacion_promedio("123")

    # Actualizar un comentario
    # actualizar_comentario("1", "Comentario actualizado")

    # Eliminar un comentario
    # eliminar_comentario("1")

if __name__ == "__main__":
    main()
