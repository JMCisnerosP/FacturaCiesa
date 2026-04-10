from flask import Flask, render_template, request
import os
import csv
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Crear la carpeta de subida si no existe
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def formulario():
    return render_template('formulario.html')

@app.route('/enviar', methods=['POST'])
def enviar():
    forma_pago, metodo_pago = request.form['forma_pago'].split('|')
    
    datos = {
        'nombre': request.form['nombre'],
        'rfc': request.form['rfc'],
        'correo': request.form['correo'],
        'uso_cfdi': request.form['uso_cfdi'],
        'monto': request.form['monto'],
	'forma_pago': forma_pago,
	'metodo_pago': metodo_pago
	
    }

    archivo = request.files['constancia']
    if archivo:
        filename = secure_filename(archivo.filename)
        archivo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        datos['archivo'] = filename
    else:
    	datos['archivo'] = ''

    csv_file = os.path.join(app.config['UPLOAD_FOLDER'], 'solicitudes_factura.csv')
    headers = ['Nombre', 'RFC', 'Correo Electrónico', 'Uso CFDI','Monto','Forma y Método de Pago', 'Fecha de Solicitud','ArchivoSubido']
    
    if not os.path.exists(csv_file):
       with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
           writer = csv.writer(file)
           writer.writerow(headers)
    
    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
	     datos['nombre'],
	     datos['rfc'],
	     datos['correo'],
	     datos['uso_cfdi'],
	     datos['monto'],
	     f"{datos['forma_pago']} - {datos['metodo_pago']}",
	     datetime.now().strftime('%Y-%m-%d'),
	     datos['archivo']
	])

    
    return render_template('confirmacion.html', datos=datos)

if __name__ == '__main__':
    app.run(debug=True)
