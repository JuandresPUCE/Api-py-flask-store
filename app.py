# Importamos las librerías necesarias
from flask import Flask, jsonify, render_template
import requests
from test_products import products

# Creamos una instancia de la aplicación Flask
app=Flask(__name__)

# Definimos la ruta raíz ("/")
@app.route('/')
def root():
    # Cuando se accede a la ruta raíz, se devuelve un mensaje de bienvenida
    return 'Bienvenido a la tienda de todo'

# Definimos una ruta de prueba ("/ping")
@app.route('/ping')
def ping():
    # Cuando se accede a "/ping", se devuelve "correcto-pong"
    return 'correcto-pong'

# Definimos la ruta de productos ("/products")
@app.route('/products', methods=['GET'])
def get_products():
    # Cuando se accede a "/products", se devuelven todos los productos en formato JSON
    #return jsonify(products)
    return render_template('guitars.html', products=products)

# Definimos la ruta de productos por nombre ("/products/<nombre_del_producto>")
@app.route('/products/<string:product_name>')
def get_product(product_name):
    # Buscamos el producto por nombre
    products_found = [product for product in products if product['name'] == product_name]
    # Si encontramos el producto, lo devolvemos en formato JSON
    if (len(products_found) > 0):
        return jsonify({"product": products_found[0]})
    # Si no encontramos el producto, devolvemos un mensaje de error
    return jsonify("mensaje: producto no encontrado :(")

@app.route('/store')
def get_store():
    # Hacemos una solicitud a la API para obtener los productos
    api_url = 'https://fakestoreapi.com/products/'
    response = requests.get(api_url)

    # Verificamos si la solicitud fue exitosa
    if response.status_code == 200:
        # Si la solicitud fue exitosa, obtenemos los datos de la respuesta en formato JSON
        products = response.json()
        # Renderizamos la plantilla 'store.html' con los productos obtenidos
        return render_template('store.html', products=products)
    else:
        # Si la solicitud no fue exitosa, devolvemos un mensaje de error
        return 'Error al obtener datos de la API', 500

# Si este script se ejecuta como el principal, iniciamos la aplicación Flask
if __name__ == '__main__':
    app.run(debug=True, port=5000)