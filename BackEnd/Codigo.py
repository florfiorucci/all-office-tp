import mysql.connector
from flask import Flask, jsonify, request
from flask_cors import CORS

# Configurar la conexión a la base de datos MySQL
DATABASE_CONFIG = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
}

DATABASE_NAME = 'B_AllOffice_bd'

def get_db_connection(database=None):
    print("Obteniendo conexión...")  # Para probar que se ejecuta la función
    config = DATABASE_CONFIG.copy()
    if database:
        config['database'] = database
    conn = mysql.connector.connect(**config)
    return conn

# Crear la tabla 'productos' si no existe
def create_table():
    print("Creando tabla productos...")  # Para probar que se ejecuta la función
    conn = get_db_connection(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            codigo INT PRIMARY KEY,
            descripcion TEXT NOT NULL,
            cantidad INT NOT NULL,
            precio DOUBLE NOT NULL
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

# Verificar si la base de datos existe, si no, crearla y crear la tabla
def create_database():
    print("Creando la Base de Datos...")  # Para probar que se ejecuta la función
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}")
    cursor.close()
    conn.close()
    create_table()

# Crear la base de datos y la tabla si no existen
create_database()

# Definimos la clase "Producto"
class Producto:
    def __init__(self, codigo, descripcion, cantidad, precio):
        self.codigo = codigo
        self.descripcion = descripcion
        self.cantidad = cantidad
        self.precio = precio

    def modificar(self, nueva_descripcion, nueva_cantidad, nuevo_precio):
        self.descripcion = nueva_descripcion
        self.cantidad = nueva_cantidad
        self.precio = nuevo_precio

# Definimos la clase "Inventario"
class Inventario:
    def __init__(self):
        self.conexion = get_db_connection(DATABASE_NAME)
        self.cursor = self.conexion.cursor()

    def agregar_producto(self, codigo, descripcion, cantidad, precio):
        producto_existente = self.consultar_producto(codigo)
        if producto_existente:
            return {'message': 'Ya existe un producto con ese código.'}, 400

        self.cursor.execute("INSERT INTO productos (codigo, descripcion, cantidad, precio) VALUES (%s, %s, %s, %s)", (codigo, descripcion, cantidad, precio))
        self.conexion.commit()
        return {'message': 'Producto agregado correctamente.'}, 200

    def consultar_producto(self, codigo):
        self.cursor.execute("SELECT * FROM productos WHERE codigo = %s", (codigo,))
        row = self.cursor.fetchone()
        if row:
            codigo, descripcion, cantidad, precio = row
            return Producto(codigo, descripcion, cantidad, precio)
        return None

    def modificar_producto(self, codigo, nueva_descripcion, nueva_cantidad, nuevo_precio):
        producto = self.consultar_producto(codigo)
        if (producto):
            producto.modificar(nueva_descripcion, nueva_cantidad, nuevo_precio)
            self.cursor.execute("UPDATE productos SET descripcion = %s, cantidad = %s, precio = %s WHERE codigo = %s",
                                (nueva_descripcion, nueva_cantidad, nuevo_precio, codigo))
            self.conexion.commit()
            return {'message': 'Producto modificado correctamente.'}, 200
        return {'message': 'Producto no encontrado.'}, 404

    def listar_productos(self):
        self.cursor.execute("SELECT * FROM productos")
        rows = self.cursor.fetchall()
        productos = []
        for row in rows:
            codigo, descripcion, cantidad, precio = row
            producto = {'Código': codigo, 'Descripción': descripcion, 'Cantidad': cantidad, 'Precio': precio}
            productos.append(producto)
        return productos, 200

    def eliminar_producto(self, codigo):
        self.cursor.execute("DELETE FROM productos WHERE codigo = %s", (codigo,))
        if self.cursor.rowcount > 0:
            self.conexion.commit()
            return {'message': 'Producto eliminado correctamente.'}, 200
        return {'message': 'Producto no encontrado.'}, 404

# Definimos la clase "Carrito"
class Carrito:
    def __init__(self):
        self.items = {}

    def agregar(self, codigo, cantidad, inventario):
        producto = inventario.consultar_producto(codigo)
        if producto:
            if codigo in self.items:
                self.items[codigo]['cantidad'] += cantidad
            else:
                self.items[codigo] = {
                    'Descripción': producto.descripcion,
                    'Cantidad': cantidad,
                    'Precio': producto.precio
                }
            return {'message': 'Producto agregado al carrito correctamente.'}, 200
        return {'message': 'Producto no encontrado en el inventario.'}, 404

    def quitar(self, codigo, cantidad, inventario):
        if codigo in self.items:
            if self.items[codigo]['Cantidad'] > cantidad:
                self.items[codigo]['Cantidad'] -= cantidad
            elif self.items[codigo]['Cantidad'] == cantidad:
                del self.items[codigo]
            else:
                return {'message': 'Cantidad a quitar excede la cantidad en el carrito.'}, 400
            return {'message': 'Producto quitado del carrito correctamente.'}, 200
        return {'message': 'Producto no encontrado en el carrito.'}, 404

    def mostrar(self):
        return jsonify(self.items), 200

# Función para insertar datos de ejemplo
def insertar_datos_de_ejemplo():
    inventario = Inventario()

    # Lista de productos de ejemplo (datos inventados)
    productos_de_ejemplo = [
        # Escritorios
        (10001, 'Escritorio Filadelfia', 10, 250000),
        (10002, 'Escritorio Oklahoma', 10, 250000),
        (10003, 'Escritorio Houston', 10, 260000),
        (10004, 'Escritorio Chicago', 10, 260000),
        (10005, 'Escritorio Detroit', 10, 280000),
        (10006, 'Escritorio Boston', 10, 280000),
        (10007, 'Escritorio Roma', 10, 250000),
        (10008, 'Escritorio Milán', 10, 260000),
        (10009, 'Escritorio Venecia', 10, 270000),
        (10010, 'Escritorio Bolonia', 10, 280000),
        (10011, 'Escritorio Génova', 10, 290000),
        (10012, 'Escritorio Verona', 10, 300000),

        # Sillas
        (20001, 'Silla Filadelfia', 20, 120000),
        (20002, 'Silla Oklahoma', 20, 130000),
        (20003, 'Silla Houston', 20, 140000),
        (20004, 'Silla Chicago', 20, 150000),
        (20005, 'Silla Detroit', 20, 160000),
        (20006, 'Silla Boston', 20, 170000),
        (20007, 'Silla Roma', 20, 120000),
        (20008, 'Silla Milán', 20, 130000),
        (20009, 'Silla Venecia', 20, 140000),
        (20010, 'Silla Bolonia', 20, 150000),
        (20011, 'Silla Génova', 20, 160000),
        (20012, 'Silla Verona', 20, 170000),

        # Archivadores
        (30001, 'Archivador Roma', 15, 80000),
        (30002, 'Archivador Milán', 15, 85000),
        (30003, 'Archivador Venecia', 15, 90000),
        (30004, 'Archivador Bolonia', 15, 95000),
        (30005, 'Archivador Génova', 15, 100000),
        (30006, 'Archivador Verona', 15, 105000),

        # Bibliotecas
        (40001, 'Biblioteca Filadelfia', 12, 500000),
        (40002, 'Biblioteca Oklahoma', 12, 550000),
        (40003, 'Biblioteca Houston', 12, 600000),
        (40004, 'Biblioteca Chicago', 12, 605000),
        (40005, 'Biblioteca Detroit', 12, 700000),
        (40006, 'Biblioteca Boston', 12, 70500)
    ]

    for producto in productos_de_ejemplo:
        codigo, descripcion, cantidad, precio = producto
        resultado, codigo_respuesta = inventario.agregar_producto(codigo, descripcion, cantidad, precio)
        if codigo_respuesta != 200:
            print(f"Error al agregar el producto {codigo}: {resultado['message']}")
        else:
            print(f"Producto {codigo} agregado correctamente.")

# Función para insertar un producto de ejemplo
def insertar_producto_ejemplo():
    inventario = Inventario()
    codigo = 50001
    descripcion = 'Lámpara de Oficina'
    cantidad = 5
    precio = 150000
    resultado, codigo_respuesta = inventario.agregar_producto(codigo, descripcion, cantidad, precio)
    if codigo_respuesta != 200:
        print(f"Error al agregar el producto {codigo}: {resultado['message']}")
    else:
        print(f"Producto {codigo} agregado correctamente.")

# Función para modificar el producto de ejemplo
def modificar_producto_ejemplo():
    inventario = Inventario()
    codigo = 50001
    nueva_descripcion = 'Lámpara de Oficina LED'
    nueva_cantidad = 10
    nuevo_precio = 200000
    resultado, codigo_respuesta = inventario.modificar_producto(codigo, nueva_descripcion, nueva_cantidad, nuevo_precio)
    if codigo_respuesta != 200:
        print(f"Error al modificar el producto {codigo}: {resultado['message']}")
    else:
        print(f"Producto {codigo} modificado correctamente.")

# Función para eliminar el producto de ejemplo
def eliminar_producto_ejemplo():
    inventario = Inventario()
    codigo = 50001
    resultado, codigo_respuesta = inventario.eliminar_producto(codigo)
    if codigo_respuesta != 200:
        print(f"Error al eliminar el producto {codigo}: {resultado['message']}")
    else:
        print(f"Producto {codigo} eliminado correctamente.")

# insertar_datos_de_ejemplo()
# insertar_producto_ejemplo()
# modificar_producto_ejemplo()
# eliminar_producto_ejemplo()

# Configuración y rutas de la API Flask
app = Flask(__name__)
CORS(app)

carrito = Carrito()
inventario = Inventario()

@app.route('/productos/<int:codigo>', methods=['GET'])
def obtener_producto(codigo):
    producto = inventario.consultar_producto(codigo)
    if producto:
        return jsonify({
            'Código': producto.codigo,
            'Descripción': producto.descripcion,
            'Cantidad': producto.cantidad,
            'Precio': producto.precio
        }), 200
    return jsonify({'message': 'Producto no encontrado.'}), 404

@app.route('/productos', methods=['GET'])
def obtener_productos():
    productos, codigo_respuesta = inventario.listar_productos()
    return jsonify(productos), codigo_respuesta

@app.route('/productos', methods=['POST'])
def agregar_producto():
    codigo = request.json.get('codigo')
    descripcion = request.json.get('descripcion')
    cantidad = request.json.get('cantidad')
    precio = request.json.get('precio')
    resultado, codigo_respuesta = inventario.agregar_producto(codigo, descripcion, cantidad, precio)
    return jsonify(resultado), codigo_respuesta

@app.route('/productos/<int:codigo>', methods=['PUT'])
def modificar_producto(codigo):
    nueva_descripcion = request.json.get('descripcion')
    nueva_cantidad = request.json.get('cantidad')
    nuevo_precio = request.json.get('precio')
    resultado, codigo_respuesta = inventario.modificar_producto(codigo, nueva_descripcion, nueva_cantidad, nuevo_precio)
    return jsonify(resultado), codigo_respuesta

@app.route('/productos/<int:codigo>', methods=['DELETE'])
def eliminar_producto(codigo):
    resultado, codigo_respuesta = inventario.eliminar_producto(codigo)
    return jsonify(resultado), codigo_respuesta

@app.route('/carrito', methods=['POST'])
def agregar_carrito():
    codigo = request.json.get('codigo')
    cantidad = request.json.get('cantidad')
    inventario = Inventario()
    return carrito.agregar(codigo, cantidad, inventario)

@app.route('/carrito', methods=['DELETE'])
def quitar_carrito():
    codigo = request.json.get('codigo')
    cantidad = request.json.get('cantidad')
    inventario = Inventario()
    return carrito.quitar(codigo, cantidad, inventario)

@app.route('/carrito', methods=['GET'])
def obtener_carrito():
    return carrito.mostrar()

@app.route('/')
def index():
    return 'API de Inventario'

if __name__ == '__main__':
    app.run()
