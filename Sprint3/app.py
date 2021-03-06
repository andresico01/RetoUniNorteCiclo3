from flask import Flask, render_template,request
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

# Clase para administrar usuarios del sistema
class Usuario:
    # Metodo constructor de la clase
    def __init__(self, email, nombre, password):
        self.email = email
        self.nombre = nombre
        self.password = password

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

# Flag de sesion activa (Variable Global)
sesion = False

# Usuario conectado (Variable Global)
usuario = None

# Listado de usuarios inicial (Variable Global)
usuarios = [Usuario("mzamoraa@uninorte.edu.co", "mzamora", "12345"), Usuario("serdnaoiram@hotmail.com", "serdna", "12")]

@app.route('/')
def home():
    return render_template("login.html", mensaje="")

@app.route('/Blog',methods=["GET", "POST"])
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


if __name__ == '__main__':
    app.run(debug=True)