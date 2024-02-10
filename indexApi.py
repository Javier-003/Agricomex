from flask import Flask, jsonify,render_template, request, redirect, session, url_for,Response,flash
import secrets
import conexionApi as db

app = Flask(__name__)


@app.route('/api/productos', methods=['GET'])
def obtener_productos():
    cursor = db.conexion.cursor()
    cursor.execute("SELECT * FROM productos")
    datosDB = cursor.fetchall()
    # convertir los datos a una lista de diccionarios
    productos = []
    columnName = [column[0] for column in cursor.description]
    for registro in datosDB:
        productos.append(dict(zip(columnName, registro)))   
    cursor.close()
    return jsonify(productos)

@app.route('/api/productos/<nombre>', methods=['GET'])
def obtener_productos_por_nombre(nombre):
    cursor = db.conexion.cursor()
    cursor.execute("SELECT * FROM productos WHERE nombre=%s",(nombre,))
    datosDB = cursor.fetchall()
    # convertir los datos a una lista de diccionarios
    productos = []
    columnName = [column[0] for column in cursor.description]
    for registro in datosDB:
        productos.append(dict(zip(columnName, registro)))   
    cursor.close()
    return jsonify(productos)
    
    
@app.route('/api/calendario', methods=['GET'])
def obtener_calendario():
    cursor = db.conexion.cursor()
    cursor.execute("SELECT * FROM calendario_fertilidad")
    datosDB = cursor.fetchall()
    # convertir los datos a una lista de diccionarios
    calendario = []
    columnName = [column[0] for column in cursor.description]
    for registro in datosDB:
        calendario.append(dict(zip(columnName, registro)))   
    cursor.close()
    return jsonify(calendario)

@app.route('/api/calendario/<estado>', methods=['GET'])
def obtener_calendario_por_estado(estado):
    cursor = db.conexion.cursor()
    cursor.execute("SELECT * FROM calendario_fertilidad WHERE estado = %s", (estado,))
    datosDB = cursor.fetchall()
    calendario = []
    columnName = [column[0] for column in cursor.description]
    for registro in datosDB:
        calendario.append(dict(zip(columnName, registro)))   
    cursor.close()
    return jsonify(calendario)
    
    
@app.route('/api/suelos', methods=['GET'])
def obtener_suelos():
    cursor = db.conexion.cursor()
    cursor.execute("SELECT * FROM suelos")
    datosDB = cursor.fetchall()
    # convertir los datos a una lista de diccionarios
    suelos = []
    columnName = [column[0] for column in cursor.description]
    for registro in datosDB:
        suelos.append(dict(zip(columnName, registro)))   
    cursor.close()
    return jsonify(suelos)

@app.route('/api/suelos/<estado>', methods=['GET'])
def obtener_suelos_por_estado(estado):
    cursor = db.conexion.cursor()
    cursor.execute("SELECT * FROM suelos WHERE estado = %s", (estado,))
    datosDB = cursor.fetchall()
    suelos = []
    columnName = [column[0] for column in cursor.description]
    for registro in datosDB:
        suelos.append(dict(zip(columnName, registro)))   
    cursor.close()
    return jsonify(suelos)
    
    
@app.route('/api/tiendas', methods=['GET'])
def obtener_tiendas():
    cursor = db.conexion.cursor()
    cursor.execute("SELECT * FROM tiendas")
    datosDB = cursor.fetchall()
    # convertir los datos a una lista de diccionarios
    tiendas = []
    columnName = [column[0] for column in cursor.description]
    for registro in datosDB:
        tiendas.append(dict(zip(columnName, registro)))   
    cursor.close()
    return jsonify(tiendas)
    
    
@app.route('/api/plagas', methods=['GET'])
def obtener_plagas():
    cursor = db.conexion.cursor()
    cursor.execute("SELECT * FROM plagas")
    datosDB = cursor.fetchall()
    # convertir los datos a una lista de diccionarios
    plagas = []
    columnName = [column[0] for column in cursor.description]
    for registro in datosDB:
        plagas.append(dict(zip(columnName, registro)))   
    cursor.close()
    return jsonify(plagas)
    
    
    

if __name__ == '__main__':
    app.run(debug=True, port=5000)