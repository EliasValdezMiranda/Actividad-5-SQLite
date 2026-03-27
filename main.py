#Integración SQLite y Flask
from flask import Flask, jsonify, request
import sqlite3

# Creación de objeto Flask
app = Flask(__name__)
app.json.sort_keys = False

# Constante con el nombre de la base de datos
NOMBRE_DB = "tienda.db"

# Función de conexión a la base de datos
def conexionDB():
    return sqlite3.connect(NOMBRE_DB)


# Método GET
@app.route("/productos", methods=["GET"])
def obtenerProductos():
    # Se crea una conexión a la base de datos y se toma un cursor de este
    conn = conexionDB()
    cursor = conn.cursor()
    
    # Se extraen todos los productos de la tabla 'productos' en la base de datos
    cursor.execute("SELECT * FROM productos")

    # Se extraen los datos del cursor y se guardan en la lista 'productos'
    datos = cursor.fetchall()
    productos = []
    for fila in datos:
        productos.append({
            "id": fila[0],
            "nombre": fila[1],
            "precio": fila[2],
            "stock": fila[3]
        })
    
    # Se cierra la conexión y se regresan los productos en formato JSON
    conn.close()
    return jsonify(productos), 200


# Método POST
@app.route("/productos", methods=["POST"])
def agregarProducto():
    # Se obtiene la información ofrecida por el usuario en formato JSON
    data = request.json
    
    # Se crea una conexión a la base de datos
    conn = conexionDB()
    
    # Se ejecuta el comando de inserción en la tabla 'productos' de la base de datos
    conn.execute("""
                    INSERT INTO productos(nombre, precio, stock)
                    VALUES(?,?,?)
                    """, (data["nombre"], data["precio"], data["stock"]))
    
    # Se confirma la modificación sobre la base de datos, se cierra la conexión y
    # se devuelve un mensaje de éxito en formato JSON
    conn.commit()
    conn.close()
    return jsonify({"mensaje":"Producto agregado"}), 201


# Método PUT
@app.route("/productos/<int:id>", methods=["PUT"])
def actualizarProducto(id):
    data = request.json

    # Se crea una conexión a la base de datos
    conn = conexionDB()
    
    # Se ejecuta el comando de actualización en la tabla 'productos' de la base de datos
    # Toma como referencia la id provista en la ruta
    conn.execute("""
                    UPDATE productos
                    SET nombre = ?, precio = ?, stock = ?
                    WHERE id = ?
                """, (data["nombre"], data["precio"], data["stock"], id))

    # Se confirma la modificación sobre la base de datos, se cierra la conexión y
    # se devuelve un mensaje de éxito en formato JSON
    conn.commit()
    conn.close()
    return jsonify({"mensaje": "Producto actualizado"}), 200


# Método DELETE
@app.route("/productos/<int:id>", methods=["DELETE"])
def eliminarProducto(id):
    # Se crea una conexión a la base de datos
    conn = conexionDB()
    
    # Se ejecuta el comando de eliminación en la tabla 'productos de la base de datos'
    # Toma como referencia la id provista en la ruta
    conn.execute("DELETE FROM productos WHERE id=?", (id,))
    
    # Se confirma la modificación sobre la base de datos, se cierra la conexión y
    # se devuelve un mensaje de éxito en formato JSON
    conn.commit()
    conn.close()
    return jsonify({"mensaje":"Producto eliminado"}), 200


# Ruta con clausula WHERE 1:
# Búsqueda de productos con nombre cercano a referencia
@app.route("/productos/filtrar/nombre/inexacto/<match>", methods=['GET'])
def filtradoBusquedaInexacta(match):
    # Se crea una conexión a la base de datos y se toma un cursor de este
    conn = conexionDB()
    cursor = conn.cursor()

    # Se buscan los productos con un nombre similar al provisto en la ruta
    cursor.execute("SELECT * FROM productos WHERE nombre LIKE ?", (f"%{match}%",))

    # Se extraen los datos del cursor y se guardan en la lista 'productos'
    datos = cursor.fetchall()
    productos = []
    for fila in datos:
        productos.append({
            "id": fila[0],
            "nombre": fila[1],
            "precio": fila[2],
            "stock": fila[3]
        })
    
    # Se cierra la conexión y se regresan los productos encontrados en formato JSON
    conn.close()
    return jsonify(productos), 200


# Ruta con clausula WHERE 2:
# Búsqueda de productos con precio menor a referencia
@app.route("/productos/filtrar/precio/menor/<int:precio>", methods=['GET'])
def filtradoPrecioMenor(precio):
    # Se crea una conexión a la base de datos y se toma un cursor de este
    conn = conexionDB()
    cursor = conn.cursor()
    
    # Se buscan los productos con un precio menor al provisto en la ruta
    cursor.execute("SELECT * FROM productos WHERE precio < ?", (precio,))

    # Se extraen los datos del cursor y se guardan en la lista 'productos'
    datos = cursor.fetchall()
    productos = []
    for fila in datos:
        productos.append({
            "id": fila[0],
            "nombre": fila[1],
            "precio": fila[2],
            "stock": fila[3]
        })
    
    # Se cierra la conexión y se regresan los productos encontrados en formato JSON
    conn.close()
    return jsonify(productos), 200


# Instrucción para empezar la aplicación Flask
app.run(debug=True)