#--------------------------------------------------------------------
# Instalar con pip install Flask
from flask import Flask, request, jsonify
from flask_cors import CORS

# Instalar con pip install mysql-connector-python
import mysql.connector

# Si es necesario, pip install Werkzeug
from werkzeug.utils import secure_filename

#--------------------------------------------------------------------

app = Flask(__name__)
CORS(app)  # Esto habilitará CORS para todas las rutas

#--------------------------------------------------------------------
class Catalogo:
    #----------------------------------------------------------------
    # Constructor de la clase
    def __init__(self, host, user, password, database):
        # Primero, establecemos una conexión sin especificar la base de datos
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        self.cursor = self.conn.cursor()

        # Intentamos seleccionar la base de datos
        try:
            self.cursor.execute(f"USE {database}")
        except mysql.connector.Error as err:
            # Si la base de datos no existe, la creamos
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f"CREATE DATABASE {database}")
                self.conn.database = database
            else:
                raise err

        # Una vez que la base de datos está establecida, creamos la tabla si no existe
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS productos (
            codigo INT AUTO_INCREMENT PRIMARY KEY,
            descripcion VARCHAR(255) NOT NULL,
            cantidad INT NOT NULL,
            precio DECIMAL(10, 2) NOT NULL,
            imagen_url VARCHAR(255),
            proveedor INT(4))''')
        self.conn.commit()

        # Cerrar el cursor inicial y abrir uno nuevo con el parámetro dictionary=True
        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)
        
    #----------------------------------------------------------------
    def agregar_producto(self, descripcion, cantidad, precio):
        sql = "INSERT INTO productos (descripcion, cantidad, precio) VALUES (%s, %s, %s)"
        valores = (descripcion, cantidad, precio)
        self.cursor.execute(sql, valores)        
        self.conn.commit()
        return self.cursor.lastrowid

    #----------------------------------------------------------------
    def consultar_producto(self, codigo):
        # Consultamos un producto a partir de su código
        self.cursor.execute(f"SELECT * FROM productos WHERE codigo = {codigo}")
        return self.cursor.fetchone()

    #----------------------------------------------------------------
    def modificar_producto(self, codigo, nueva_descripcion, nueva_cantidad, nuevo_precio):
        sql = "UPDATE productos SET descripcion = %s, cantidad = %s, precio = %s WHERE codigo = %s"
        valores = (nueva_descripcion, nueva_cantidad, nuevo_precio, codigo)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.rowcount > 0

    #----------------------------------------------------------------
    def listar_productos(self):
        self.cursor.execute("SELECT * FROM productos")
        productos = self.cursor.fetchall()
        return productos

    #----------------------------------------------------------------
    def eliminar_producto(self, codigo):
        # Eliminamos un producto de la tabla a partir de su código
        self.cursor.execute(f"DELETE FROM productos WHERE codigo = {codigo}")
        self.conn.commit()
        return self.cursor.rowcount > 0

#--------------------------------------------------------------------
# Cuerpo del programa
#--------------------------------------------------------------------
# Crear una instancia de la clase Catalogo
catalogo = Catalogo(host='Lenny896.mysql.pythonanywhere-services.com', user='Lenny896', password='leoo0037', database='Lenny896$b_alloffice_bd')
#catalogo = Catalogo(host='USUARIO.mysql.pythonanywhere-services.com', user='USUARIO', password='CLAVE', database='USUARIO$miapp')


# Carpeta para guardar las imagenes.
RUTA_DESTINO = '/home/Lenny896/mysite/static/img/'

#Al subir al servidor, deberá utilizarse la siguiente ruta. USUARIO debe ser reemplazado por el nombre de usuario de Pythonanywhere
#RUTA_DESTINO = '/home/USUARIO/mysite/static/imagenes'

#--------------------------------------------------------------------
# Listar todos los productos
#--------------------------------------------------------------------
@app.route("/productos", methods=["GET"])
def listar_productos():
    productos = catalogo.listar_productos()
    return jsonify(productos)

#--------------------------------------------------------------------
# Mostrar un sólo producto según su código
#--------------------------------------------------------------------
@app.route("/productos/<int:codigo>", methods=["GET"])
def mostrar_producto(codigo):
    producto = catalogo.consultar_producto(codigo)
    if producto:
        return jsonify(producto), 200
    else:
        return "Producto no encontrado", 404

#--------------------------------------------------------------------
# Agregar un producto
#--------------------------------------------------------------------
@app.route("/productos", methods=["POST"])
def agregar_producto():
    descripcion = request.form.get('descripcion')
    cantidad = request.form.get('cantidad')
    precio = request.form.get('precio')
    
    if not descripcion or not cantidad or not precio:
        return jsonify({"mensaje": "Datos incompletos"}), 400

    try:
        nuevo_codigo = catalogo.agregar_producto(descripcion, cantidad, precio)
        return jsonify({"mensaje": "Producto agregado correctamente.", "codigo": nuevo_codigo}), 201
    except Exception as e:
        return jsonify({"mensaje": f"Error al agregar el producto: {str(e)}"}), 500

#--------------------------------------------------------------------
# Modificar un producto según su código
#--------------------------------------------------------------------
@app.route("/productos/<int:codigo>", methods=["PUT"])
def modificar_producto(codigo):
    nueva_descripcion = request.form.get("descripcion")
    nueva_cantidad = request.form.get("cantidad")
    nuevo_precio = request.form.get("precio")

    if not nueva_descripcion or not nueva_cantidad or not nuevo_precio:
        return jsonify({"mensaje": "Datos incompletos"}), 400

    if catalogo.modificar_producto(codigo, nueva_descripcion, nueva_cantidad, nuevo_precio):
        return jsonify({"mensaje": "Producto modificado"}), 200
    else:
        return jsonify({"mensaje": "Producto no encontrado"}), 404

#--------------------------------------------------------------------
# Eliminar un producto según su código
#--------------------------------------------------------------------
@app.route("/productos/<int:codigo>", methods=["DELETE"])
def eliminar_producto(codigo):
    producto = catalogo.consultar_producto(codigo)
    if producto:
        if catalogo.eliminar_producto(codigo):
            return jsonify({"mensaje": "Producto eliminado"}), 200
        else:
            return jsonify({"mensaje": "Error al eliminar el producto"}), 500
    else:
        return jsonify({"mensaje": "Producto no encontrado"}), 404

#--------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
