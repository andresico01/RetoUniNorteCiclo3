from flask import Flask, render_template,request,session,redirect,url_for
import sqlite3
import sqlite3 as sql
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
""" 
# Clase para administrar usuarios del sistema
class Usuario:
    # Metodo constructor de la clase
    def __init__(self, email, nombre, password):
        self.email = email
        self.nombre = nombre
        self.password = password
 """
# Clase para administrar mensajes del sistema
class Mensaje:
    # Metodo constructor de la clase
    def __init__(self, titulo, texto, esError):
        #self.css = css
        self.titulo = titulo
        self.texto = texto
        self.esError = esError


app = Flask(__name__)
msg = MIMEMultipart()

""" # Flag de sesion activa (Variable Global)
sesion = False

# Usuario conectado (Variable Global)
usuario = None

# Listado de usuarios inicial (Variable Global)
#usuarios = [Usuario("mzamoraa@uninorte.edu.co", "mzamora", "12345"), Usuario("serdnaoiram@hotmail.com", "serdna", "12")]
 """
@app.route('/')
def home():
    return redirect(url_for('acceso'))

@app.route('/acceso')
def acceso():
    mensaje = Mensaje("", "", False)
    return render_template('login.html', mensaje=mensaje)

@app.route('/login',methods=['GET','POST'])
def login():
    contador = 0
    
    if(request.method == 'POST'):
        correo = request.form['correo']
        passw = request.form['contraseña']
        conexion = sqlite3.connect("dbUsuarios.db")
        conexion.row_factory = sql.Row
   
        objcursor = conexion.cursor()
        objcursor.execute("select * from T_Usuarios where Correo = '"+correo+"' and Pass = '"+passw+"'")
        rows = objcursor.fetchall()
    
        for i in rows:
            contador = contador + 1
                
        if(contador > 0):
            print(contador)
            session['login'] = True
            session['user'] = correo
            #return redirect(url_for('principal',user=correo))
            return render_template('RealBlog.html', user=correo)
        else:
            mensaje = Mensaje("!ERROR¡", "Correo Electronico y/o Contraseña estan errados.", True)
        return render_template('login.html', mensaje = mensaje)
    

app.secret_key = '1234'

@app.route('/RealBlog')
def principal():
    if 'user' in session:
        return render_template('/RealBlog.html')
    else:
        mensaje = Mensaje("!ERROR¡", "Por Favor Inicie Sesión.", True)
        return render_template('/login.html',mensaje=mensaje)

@app.route('/logout')
def logout():
    if 'user' in session:
        session.clear()
        session.pop('user', None)
        return redirect(url_for('acceso'))
    else:
        mensaje = Mensaje("!ERROR¡","Debes Iniciar Sesión Primero",True)
        return render_template('login.html',mensaje=mensaje)

@app.route('/formulario')
def regist():
    mensaje = Mensaje("", "", False)
    return render_template("formulario.html", mensaje = mensaje)

@app.route('/formulario', methods=["GET", "POST"])
def registro():
    email = request.form['correo']
    usuario = request.form['usuario']
    contraseña = request.form['contraseña']
    contraseña2 = request.form['contraseña2']
    found = False
    contador =0
    mensaje = Mensaje("", "", False)
    if contraseña != contraseña2:
        mensaje = Mensaje( "!ERROR¡", "Las contraseñas no coinciden", True)
        print(mensaje.titulo)
        return render_template("formulario.html", mensaje=mensaje)
    
    if found == False:
#REVISAR ESTA LOGICA...ENVIA MENSAJE DE EXITENCIA DE UN CORREO,Y DEBERIA SOEIAR NOTIFICACION DE
# SE ENIARA UN CORREO CON SUS DATOS DE ACCESO,Y EN CASO DE POSIBLE HACKEO NOTIFICAR AL USUARIO
# QUE ESTAN INTENTADO REGISTRASRSE CON SU CORREO EN EL BLOG        
        conexion = sqlite3.connect("dbUsuarios.db")
        conexion.row_factory = sql.Row
   
        objcursor = conexion.cursor()
        objcursor.execute("select * from T_Usuarios where Correo = '"+email+"'")
        rows = objcursor.fetchall()
        conexion.close()

        for i in rows:
            print(i[0])
            contador = contador+1
        if contador > 0:
            #usuario = usr
            found = True

            # Envio correo notificando a usuario actioelinteto de creacion de cuenta con su dirrecion de correo electronico
            message_e = "Alguien esta intentando crear una cuenta con tu direcciín de correo electronico\n\n Si has sido tu y deseas recordar tu contraseña puedes hacerlo a travez del siguiente enlace:\n\nhttp://127.0.0.1:5000/Contr ."
            #parametros de conexión del correo electronico
            password = "grupo2ooma"
            msg['From'] = "grupo.2.0.uninorte2020@gmail.com"
            msg['To'] = email
            msg['Subject'] = "Intento de creación de cuenta"
            # Cuerpo del mensaje se escoje texto plano
            msg.attach(MIMEText(message_e, 'plain'))
            #establecer conexión con el servidor en este caso gmail
            server = smtplib.SMTP('smtp.gmail.com: 587')
            server.starttls()
            #autenticación de las credenciales de correo con el servidor de gmail
            server.login(msg['From'], password)
            #enviar el mensaje a travez del servidor de correo de gmail
            server.sendmail(msg['From'], msg['To'], msg.as_string())
            server.quit()#cerrar la conexión con el servidor
            mensaje = Mensaje("NOTIFICACION","Te enviamos un correo con los datos de acceso para tu cuenta", True)
            return render_template('/formulario.html', mensaje=mensaje)

            #mensaje = Mensaje("!ERROR¡", "Existe un usuario registrado con este correo electronico.", True)
            #return render_template("formulario.html", mensaje=mensaje)
            #break
        # REVISAR PARA CERRAR CONEXION CON BASE DE DATOS conexion.close()

    if found == False:
        #conexion con base de datos y registro de usuario    
        conexion = sqlite3.connect("dbUsuarios.db")
        conexion.execute("insert into T_Usuarios(Correo,Pass,Nom_Usuario) values (?,?,?)" ,(email,contraseña,usuario))
        conexion.commit()
        conexion.close()
        
        # Envio correo condatosde cuenta
        message_e = "Gracias por utilizar nuestro servicio de Blos\n\nCorreo: "+email+"\nUsuario: "+usuario+"\nContraseña: "+contraseña+"\n\n Esperamos que nuestros servicios sean de tu agrado."
        #parametros de conexión del correo electronico
        password = "grupo2ooma"
        msg['From'] = "grupo.2.0.uninorte2020@gmail.com"
        msg['To'] = email
        msg['Subject'] = "Registro de Usuario"
        # Cuerpo del mensaje se escoje texto plano
        msg.attach(MIMEText(message_e, 'plain'))
        #establecer conexión con el servidor en este caso gmail
        server = smtplib.SMTP('smtp.gmail.com: 587')
        server.starttls()
        #autenticación de las credenciales de correo con el servidor de gmail
        server.login(msg['From'], password)
        #enviar el mensaje a travez del servidor de correo de gmail
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()#cerrar la conexión con el servidor
        #PENDIENTE CAMBIARETE MENSAJE POR ==>mensaje = Mensaje("NOTIFICACION","Te enviamos un correo con los datos de acceso para tu cuenta", True)
        mensaje = Mensaje("REGISTRO EXITOSO","Te enviamos un correo con tus datos de acceso intenta ingresar a tu cuenta", True)
        return render_template('/formulario.html', mensaje=mensaje)


""" @app.route('/Blog',methods=["GET", "POST"])
def login():
    # Declaracion para uso de variables globales
    global sesion
    global usuario
    # Si la sesion esta activa se redirige a la vista de tareas
    if sesion:
         return render_template("Blog.html", usuario=usuario)
    mensaje = Mensaje("", "", False)
    # Se verifica que verbo HTTP se utilizo para la peticion. Si es POST es el formulario, si es GET es desde la URL
    if request.method == "GET":
        return render_template("login.html", mensaje=mensaje)
    else:
        # Se obtienen los datos del formulario
        email = request.form.get("correo")
        password = request.form.get("contraseña")
        
        # Se busca si el usuario se encuentra registrado y su contraseña esta correcta
        found = False
        for usr in usuarios:
             if usr.email == email and usr.password == password:
                  usuario = usr
                  found = True
                  break

        # Validacion del usuario
        if found:
             sesion = True
             return render_template("Blog.html")
        else:
             mensaje = Mensaje("Validación", "Correo Electronico y/o Contraseña estan errados.", True)
             print(mensaje.titulo)
             return render_template("login.html", mensaje=mensaje)


@app.route('/formulario.html')
def regist():
    mensaje = Mensaje("", "", False)
    return render_template("formulario.html", mensaje = mensaje)    

@app.route('/formulario.html', methods=["GET", "POST"])
def registro():
    email = request.form['correo']
    usuario = request.form['usuario']
    contraseña = request.form['contraseña']
    contraseña2 = request.form['contraseña2']
    found = False
    mensaje = Mensaje("", "", False)
    if contraseña != contraseña2:
        mensaje = Mensaje( "Validación", "Las contraseñas no coinciden.", True)
        print(mensaje.titulo)
        return render_template("formulario.html", mensaje=mensaje)
    elif found == False:
        for usr in usuarios:
            if usr.email == email:
                #usuario = usr
                found = True
                mensaje = Mensaje("Validación", "Existe un usuario registrado con este correo electronico.", True)
                return render_template("formulario.html", mensaje=mensaje)
                break
    if found == False:
        usuarios.extend([Usuario(email, usuario, contraseña)])
        message_e = "Gracias por utilizar nuestro servicio de Blos\n\nCorreo: "+email+"\nUsuario: "+usuario+"\nContraseña: "+contraseña+"\n\n Esperamos que nuestros servicios sean de tu agrado."
        #parametros de conexión del correo electronico
        password = "grupo2ooma"
        msg['From'] = "grupo.2.0.uninorte2020@gmail.com"
        msg['To'] = email
        msg['Subject'] = "Registro de Usuarios"
        # Cuerpo del mensaje se escoje texto plano
        msg.attach(MIMEText(message_e, 'plain'))
        #establecer conexión con el servidor en este caso gmail
        server = smtplib.SMTP('smtp.gmail.com: 587')
        server.starttls()
        #autenticación de las credenciales de correo con el servidor de gmail
        server.login(msg['From'], password)
        #enviar el mensaje a travez del servidor de correo de gmail
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()#cerrar la conexión con el servidor
        mensaje = Mensaje("Validacion","Usuario registrado con exito", True)
        return render_template('/formulario.html', mensaje=mensaje)
   
    return render_template("/login.html")
    

@app.route('/Contr.html')
def contr():
    mensaje = Mensaje("", "", False)
    return render_template("/Contr.html", mensaje=mensaje)


@app.route('/Contr.html', methods=["GET", "POST"])
def contras():
    email = request.form['correo']
    found = False
    if found == False:
       for usr in usuarios:
            if usr.email == email:
                contraseña = usr.password
                found = True
                print(contraseña)
                
                message_e = "Gracias por utilizar nuestro servicio de Blogs, la contraseña asignada a su cuenta es:\n\nContraseña: "+contraseña+"\n\n Esperamos que nuestros servicios sean de tu agrado."+"\n\n Ahora podras disfrutar nuevamente de nuestros servicios."+"\n\n Gracias por elegirnos."
                #parametros de conexión del correo electronico
                password = "grupo2ooma"
                msg['From'] = "grupo.2.0.uninorte2020@gmail.com"
                msg['To'] = email
                msg['Subject'] = "Recuperación de contraseña"
                # Cuerpo del mensaje se escoje texto plano
                msg.attach(MIMEText(message_e, 'plain'))
                #establecer conexión con el servidor en este caso gmail
                server = smtplib.SMTP('smtp.gmail.com: 587')
                server.starttls()
                #autenticación de las credenciales de correo con el servidor de gmail
                server.login(msg['From'], password)
                #enviar el mensaje a travez del servidor de correo de gmail
                server.sendmail(msg['From'], msg['To'], msg.as_string())
                server.quit()#cerrar la conexión con el servidor
                
                mensaje = Mensaje("Validación", "Revise su correo electronico e intente ingresar nuevamente.", True)
                return render_template("/Contr.html", mensaje=mensaje)
                break
    return render_template("/Contr.html", mensaje=mensaje)

@app.route('/Blog.html')
def princip():
    return render_template("/Blog.html")
 """

if __name__ == '__main__':
    app.run(debug=True)