from flask import Flask, jsonify,render_template, request, redirect, session, url_for,Response,flash
import secrets
import conexion as db

app = Flask(__name__)

app.secret_key = 'M0i1Xc$GfPw3Yz@2SbQ9lKpA5rJhDtE7'
#####################################################################
##
@app.route('/generar_api_key',methods=["GET","POST"])
def generar_api_key():
    if request.method == 'POST':
        nueva_api_key = secrets.token_hex(16)

        # Insertar la nueva API key en la base de datos
        if nueva_api_key:
            cursor = db.conexion.cursor()
            sql = "INSERT INTO apikey (llave) VALUES (%s)"
            datos = (nueva_api_key,)
            cursor.execute(sql, datos)
            db.conexion.commit()

        # Devolver la API key como respuesta JSON
        llave=nueva_api_key
        tipollave="llave"
    return render_template("Inicio.html", llave=llave,tipollave=tipollave)
#####################################################################
@app.route('/Login', methods=["GET","POST"])
def Login():
    if request.method == 'POST':
        correo = request.form.get('txtcorreo')
        contraseña = request.form.get('txtcontraseña')

        # Aquí asumimos que "connection" es un objeto de conexión MySQL ya configurado
        cursor = db.conexion.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE correro = %s AND contraseña = SHA2(%s, 256)", (correo, contraseña))
        account = cursor.fetchone()
        cursor.close()

        if account:
            session['logueado'] = True
            session['id_rol'] = account[0]

            if session['id_rol']== 1:
                return redirect('/Adminstrador')
            else:
                return redirect('/')
        else:
            # Si no se encuentra la cuenta, muestra el mensaje de error en el modal
            mensaje = "Correo o contraseña incorrecto"
            tipo_mensaje = "error"
            return render_template("inicio_sesion.html", mensaje=mensaje, tipo_mensaje=tipo_mensaje)

    return render_template("inicio_sesion.html")

@app.route('/logout')
def logout():
    session.clear()  # Elimina todas las variables de sesión
    return redirect('/Login') # Redirige al inicio de sesión

##########################################################################

@app.route('/Adminstrador',methods=['GET'])
def Adminstrador():
    insertObjeto = []
    if 'logueado' in session and session['logueado'] and 'id_rol' in session and session['id_rol'] == 1:
            
        return render_template('MenuAdmin.html', datos=insertObjeto)
    else:
        return redirect('/Login')


@app.route('/')
def Inicio():
            
    return render_template('Inicio.html')



@app.route('/acercade')
def acercade():
    return render_template('Acerca de.html')

@app.route('/llamadas_get')
def llamadas_get():
    return render_template('llamdas.html')


##########################################################################

#Parte de productos
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

@app.route('/productos')
def productos():
    if 'logueado' in session and session['logueado'] and 'id_rol' in session and session['id_rol'] == 1:
        cursor = db.conexion.cursor()
        cursor.execute("SELECT * FROM productos")
        datosDB = cursor.fetchall()
        # convertir los datos a diccionario
        insertObjeto = []
        columnName = [column[0] for column in cursor.description]
        for registro in datosDB:
            insertObjeto.append(dict(zip(columnName, registro)))   
        cursor.close()
        return render_template('productos.html', data=insertObjeto)
    else:
        # Redirige al inicio de sesión si el usuario no ha iniciado sesión o no tiene el rol correcto
        return redirect('/Login')


@app.route('/insertproducto', methods=['POST'])
def insertproducto():
    # importamos las variables desde el form del index.htlm
    nombre = request.form["nombre_P"]
    descripcion = request.form["descripcion_P"]
    precio = request.form["precio_P"]
    categoria = request.form["categoria_P"]
    if nombre and descripcion and precio and categoria:
     cursor = db.conexion.cursor()
     sql = """INSERT INTO productos (nombre,descripcion,precio,categoria) values (%s,%s,%s,%s)"""
    # declaramos a "datos" como una variable de tipo tupla para mandar la información
    datos = (nombre, descripcion,precio,categoria)
    cursor.execute(sql, datos)
    db.conexion.commit()
    return redirect(url_for("productos"))

@app.route('/actualizarproducto/<string:id>',methods=['POST'])
def actualizarproducto(id):
    Nuevo_precio=request.form["Nuevo_P"]
    if Nuevo_precio:
        cursor = db.conexion.cursor()
        sql="""UPDATE productos
        SET precio=%s
        WHERE id=%s"""
    # declaramos a "datos" como una variable de tipo tupla para mandar la información
    datos = (Nuevo_precio,id)
    cursor.execute(sql, datos)
    db.conexion.commit()
    return redirect(url_for("productos"))

@app.route('/eliminarproducto/<string:id>')
def eliminarproducto(id):
    cursor = db.conexion.cursor()
    sql = """ DELETE FROM productos WHERE id=%s"""
    # declaramos a "datos" como una variable de tipo tupla para mandar la información
    datos = (id,)
    cursor.execute(sql, datos)
    db.conexion.commit()
    return redirect(url_for("productos"))
##########################################################################
#PARTE CALENDARIO

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

@app.route('/calendario')
def calendario():
    if 'logueado' in session and session['logueado'] and 'id_rol' in session and session['id_rol'] == 1:
     cursor = db.conexion.cursor()
     cursor.execute("SELECT * FROM calendario_fertilidad")
     datosDB = cursor.fetchall()
     # convertir los datos a diccionario
     insertObjeto = []
     columnName = [column[0] for column in cursor.description]
     for registro in datosDB:
         insertObjeto.append(dict(zip(columnName, registro)))   
     cursor.close()
     return render_template('calendario.html',data=insertObjeto)
    else:
        # Redirige al inicio de sesión si el usuario no ha iniciado sesión o no tiene el rol correcto
        return redirect('/Login')


@app.route('/insertCalendario', methods=['POST'])
def insertCalendario():
    # importamos las variables desde el form del index.htlm
    estado = request.form["estado"]
    fecha = request.form["fecha"]
    duracion = request.form["duracion"]
    dias = request.form["dias"]
    if estado and fecha and duracion:
     cursor = db.conexion.cursor()
     sql = """INSERT INTO calendario_fertilidad (estado,fecha_inicio_ciclo,duracion_ciclo,dias_fertiles) values (%s,%s,%s,%s)"""
    # declaramos a "datos" como una variable de tipo tupla para mandar la información
    datos = (estado,fecha,duracion,dias)
    cursor.execute(sql, datos)
    db.conexion.commit()
    return redirect(url_for("calendario"))

@app.route('/actualizarCalendario/<string:id>',methods=['POST'])
def actualizarCalendario(id):
    Nueva_fecha_inicio=request.form["fechaN"]
    Nuevo_ciclo=request.form["duracionN"]
    Nuevo_dias=request.form["diasN"]
    if  Nueva_fecha_inicio and Nuevo_ciclo:
        cursor = db.conexion.cursor()
        sql="""UPDATE calendario_fertilidad
        SET fecha_inicio_ciclo=%s,duracion_ciclo=%s,dias_fertiles=%s
        WHERE id=%s"""
    # declaramos a "datos" como una variable de tipo tupla para mandar la información
    datos = (Nueva_fecha_inicio,Nuevo_ciclo,Nuevo_dias,id)
    cursor.execute(sql, datos)
    db.conexion.commit()
    return redirect(url_for("calendario"))

@app.route('/eliminarfecha/<string:id>')
def eliminarfecha(id):
    cursor = db.conexion.cursor()
    sql = """ DELETE FROM calendario_fertilidad WHERE id=%s"""
    # declaramos a "datos" como una variable de tipo tupla para mandar la información
    datos = (id,)
    cursor.execute(sql, datos)
    db.conexion.commit()
    return redirect(url_for("calendario"))


##########################################################################
#PARTE SUELOS

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

@app.route('/Suelos')
def Suelos():
    if 'logueado' in session and session['logueado'] and 'id_rol' in session and session['id_rol'] == 1:
     cursor = db.conexion.cursor()
     cursor.execute("SELECT * FROM suelos")
     datosDB = cursor.fetchall()
     # convertir los datos a diccionario
     insertObjeto = []
     columnName = [column[0] for column in cursor.description]
     for registro in datosDB:
         insertObjeto.append(dict(zip(columnName, registro)))   
     cursor.close()
     return render_template('Suelos.html',data=insertObjeto)
    else:
        # Redirige al inicio de sesión si el usuario no ha iniciado sesión o no tiene el rol correcto
        return redirect('/Login')

@app.route('/ingresarSuelos', methods=['POST'])
def ingresarSuelos():
    estado = request.form["estadoS"]
    tipo_suelo = request.form["tipoSuelo"]
    dato_humedad = request.form["datosHumedad"]
    recomendacion = request.form["recomendacion"]

    if tipo_suelo and estado and dato_humedad and recomendacion:
     cursor = db.conexion.cursor()
     sql = """INSERT INTO suelos (tipo_suelo,estado,datos_humedad_suelo,recomendaciones_cultivos) values (%s,%s,%s,%s)"""
    # declaramos a "datos" como una variable de tipo tupla para mandar la información
    datos = (tipo_suelo,estado,dato_humedad,recomendacion)
    cursor.execute(sql, datos)
    db.conexion.commit()
    return redirect(url_for("Suelos"))    

@app.route('/editarSuelos/<string:id>', methods=['POST'])
def editarSuelos(id):
    dato_humedadN = request.form["datosHumedadN"]
    if  dato_humedadN:
        cursor = db.conexion.cursor()
        sql="""UPDATE suelos
        SET datos_humedad_suelo=%s
        WHERE id=%s"""
    # declaramos a "datos" como una variable de tipo tupla para mandar la información
    datos = (dato_humedadN,id)
    cursor.execute(sql, datos)
    db.conexion.commit()
    return redirect(url_for("Suelos"))

@app.route('/eliminarSuelos/<string:id>')
def eliminarSuelos(id):
    cursor = db.conexion.cursor()
    sql = """ DELETE FROM suelos WHERE id=%s"""
    # declaramos a "datos" como una variable de tipo tupla para mandar la información
    datos = (id,)
    cursor.execute(sql, datos)
    db.conexion.commit()
    return redirect(url_for("Suelos"))

##########################################################################

@app.route('/Tiendas')
def Tiendas():
    cursor = db.conexion.cursor()
    cursor.execute("SELECT * FROM tiendas")
    datosDB = cursor.fetchall()
    # convertir los datos a diccionario
    insertObjeto = []
    columnName = [column[0] for column in cursor.description]
    for registro in datosDB:
        insertObjeto.append(dict(zip(columnName, registro)))   
    cursor.close()
    return render_template('Tiendas.html',data=insertObjeto)


@app.route('/editarTienda/<string:id>',methods=['POST'])
def editarTienda(id):
    ubicacionN= request.form["ubicacionN"]
    informacionN= request.form["InformaciónN"]	
    horarioN= request.form["horarioN"]

    
    if  ubicacionN or informacionN or horarioN:
        cursor = db.conexion.cursor()
        sql="""UPDATE tiendas
        SET ubicacion=%s, informacion_contacto=%s, horario_atencion=%s  
        WHERE id=%s"""
    # declaramos a "datos" como una variable de tipo tupla para mandar la información
    datos = (ubicacionN,informacionN,horarioN,id)
    cursor.execute(sql, datos)
    db.conexion.commit()
    return redirect(url_for("Tiendas"))
    
    

@app.route ('/ingresarTienda',methods=['POST'])
def ingresarTienda():

    Nombre= request.form["nombreT"]	
    ubicacion= request.form["ubicacion"]
    informacion= request.form["Información"]	
    horario= request.form["horario"]
    

    if Nombre and ubicacion and informacion and horario:
     cursor = db.conexion.cursor()
     sql = """INSERT INTO tiendas (nombre_tienda,ubicacion,informacion_contacto,horario_atencion) values (%s,%s,%s,%s)"""
    # declaramos a "datos" como una variable de tipo tupla para mandar la información
    datos = (Nombre,ubicacion,informacion,horario)
    cursor.execute(sql, datos)
    db.conexion.commit()

    return redirect(url_for("Tiendas")) 



@app.route('/eliminarTienda/<string:id>')
def eliminarTienda(id):
    cursor = db.conexion.cursor()
    sql = """ DELETE FROM tiendas WHERE id=%s"""
    # declaramos a "datos" como una variable de tipo tupla para mandar la información
    datos = (id,)
    cursor.execute(sql, datos)
    db.conexion.commit()
    return redirect(url_for("Tiendas"))


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
##########################################################################


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

@app.route('/Plagas')
def Plagas():
    cursor = db.conexion.cursor()
    cursor.execute("SELECT * FROM plagas")
    datosDB = cursor.fetchall()
    # convertir los datos a diccionario
    insertObjeto = []
    columnName = [column[0] for column in cursor.description]
    for registro in datosDB:
        insertObjeto.append(dict(zip(columnName, registro)))   
    cursor.close()
    return render_template('Plagas.html',data=insertObjeto)

@app.route('/editarPlaga',methods=['POST'])
def editarPlaga():
    
    return redirect(url_for("Plagas"))

@app.route ('/ingresarPlaga',methods=['POST'])
def ingresarPlaga():
    Nombre= request.form["nombreP"]	
    Descripción= request.form["descripcionP"]
    Métodos_Control= request.form["metodosP"]	
    Productos= request.form["productosP"]
    Signos= request.form["signosP"]

    if Nombre and Descripción and Métodos_Control and Productos and Signos:
     cursor = db.conexion.cursor()
     sql = """INSERT INTO plagas (nombre_plaga,descripcion,metodos_control,productos_recomendados,signos_infestacion) values (%s,%s,%s,%s,%s)"""
    # declaramos a "datos" como una variable de tipo tupla para mandar la información
    datos = (Nombre,Descripción,Métodos_Control,Productos,Signos)
    cursor.execute(sql, datos)
    db.conexion.commit()
    return redirect(url_for("Plagas")) 
    

@app.route('/eliminarPlaga/<string:id>')
def eliminarPlaga(id):
    cursor = db.conexion.cursor()
    sql = """ DELETE FROM plagas WHERE id=%s"""
    # declaramos a "datos" como una variable de tipo tupla para mandar la información
    datos = (id,)
    cursor.execute(sql, datos)
    db.conexion.commit()
    return redirect(url_for("Plagas"))


##########################################################################
@app.route('/Registro')
def Registro():
    return render_template('registro.html')

@app.route('/RegistroU',methods=['POST'])
def RegistroU():
    nombre = request.form["nombre"]
    correo = request.form["correo"]
    contraseña = request.form["contraseña"]

    if nombre and correo and contraseña:
     cursor = db.conexion.cursor()
      # Verificar si el correo electrónico ya existe en la base de datos
     sql_verificar_correo = "SELECT COUNT(*) FROM usuarios WHERE correro = %s"
     cursor.execute(sql_verificar_correo, (correo,))
     num_registros = cursor.fetchone()[0]

    if num_registros > 0:
        mensaje = "Correo ya en uso"
        tipo_mensaje = "error"
        return render_template("registro.html", mensaje=mensaje, tipo_mensaje=tipo_mensaje)
    else:
        sql = """INSERT INTO usuarios (usuario, correro, contraseña, id_rol) VALUES (%s, %s, SHA2(%s, 256), 2)"""
        datos = (nombre, correo, contraseña)
        cursor.execute(sql, datos)
        db.conexion.commit()
        mensaje = "Registro hecho de manera exitosa"
        tipo_mensaje = "exito"

        return render_template("registro.html", mensaje=mensaje, tipo_mensaje=tipo_mensaje)


##########################################################################


if __name__ == '__main__':
    app.run(debug=True, port=4000)
