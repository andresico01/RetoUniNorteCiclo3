from flask import Flask, render_template,request,session,redirect,url_for
from werkzeug.security import generate_password_hash,check_password_hash
import sqlite3
import sqlite3 as sql
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

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

@app.route('/')
def home():
    return redirect(url_for('acceso'))

@app.route('/acceso')
def acceso():
    mensaje = Mensaje("", "", False)
    return render_template('login.html', mensaje=mensaje)

@app.route('/login',methods=['GET','POST'])
def login():
    #contador = 0
    
    if(request.method == 'POST'):
        correo = request.form['correo']
        passw = request.form['contraseña']
        conexion = sqlite3.connect("dbUsuarios.db")
        conexion.row_factory = sql.Row
        objcursor = conexion.cursor()
        objcursor.execute("select Hash from T_Usuarios where Correo = '"+correo+"'")
        rows = objcursor.fetchone()
            
        if passw and check_password_hash(rows["Hash"], passw):
            session['login'] = True
            session['user'] = correo
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
@app.route('/Blog')
def Blog():
    return render_template('Blog.html')



@app.route('/formulario')
def regist():
    mensaje = Mensaje("", "", False)
    return render_template("formulario.html", mensaje = mensaje)

@app.route('/formulario', methods=["POST"])
def registro():
    email= None
    email = request.form['correo']
    usuario = request.form['usuario']
    contraseña = request.form['contraseña']
    contraseña2 = request.form['contraseña2']
    valor_hash = generate_password_hash(contraseña)
    found = False
    contador =0
    mensaje = Mensaje("", "", False)

    if contraseña != contraseña2:
        mensaje = Mensaje( "!ERROR¡", "Las contraseñas no coinciden", True)
        print(mensaje.titulo)
        return render_template("formulario.html", mensaje=mensaje)
    
    if found == False:
        #conexion con base de datos y registro de usuario    
        conexion = sqlite3.connect("dbUsuarios.db")
        conexion.row_factory = sql.Row
        objcursor = conexion.cursor()
        objcursor.execute("select Pass from T_Usuarios where Correo = '"+email+"'")
        rows = objcursor.fetchall()
        conexion.close()

        if len(rows) > 0:
            contador = contador+1

        #solicitud de usuario con correo ya registrado en la base de datos    
        if contador > 0:
            
            found = True
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

    #Creacion de usuario nuevo
    if found == False:
        #conexion con base de datos y registro de usuario    
        conexion = sqlite3.connect("dbUsuarios.db")
        conexion.execute("insert into T_Usuarios(Correo,Pass,Hash,Nom_Usuario) values (?,?,?,?)" ,(email,contraseña,valor_hash,usuario))
        conexion.commit()
        conexion.close()
        
        # Envio correo con datos de cuenta
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

@app.route('/Contr')
def contr():
    mensaje =Mensaje("","",False)
    return render_template('/Contr.html', mensaje=mensaje)

@app.route('/Contr', methods=["POST"])
def contras():
    contador= 0
    email = request.form['correo']
    found = False
    if found == False:

        #conexion con base de datos y registro de usuario    
        conexion = sqlite3.connect("dbUsuarios.db")
        conexion.row_factory = sql.Row
        objcursor = conexion.cursor()
        objcursor.execute("select * from T_Usuarios where Correo = '"+email+"'")
        rows = objcursor.fetchall()
                
        if len(rows) > 0: 
            #existe el correo en la base de datos
            objcursor.execute("select * from T_Usuarios where Correo = '"+email+"'")
            rows = objcursor.fetchone()
            #contador = contador+1 
            conexion.close()
            
            message_e = "Gracias por utilizar nuestra pagina de Blogs, la contraseña asignada a tu cuenta es:\n\nContraseña: "+rows["Pass"]+"\n\n Esperamos que nuestros servicios sean de tu agrado."+"\n\n Ahora podras disfrutar nuevamente en nuestra comunidad"+"\n\n Gracias por elegirnos."
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
                
            mensaje = Mensaje("Validación", "Revisa tu correo electronico e intenta ingresar nuevamente.", True)
            return render_template("/Contr.html", mensaje=mensaje)
        
        else: 
            #no existe elcorreo en la base de datos
            conexion.close()
            mensaje = Mensaje("Validación", "usuario no registrado.", True)
            return render_template("/Contr.html", mensaje=mensaje)



if __name__ == '__main__':
    app.run(debug=True)