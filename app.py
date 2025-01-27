from flask import Flask, render_template, request, send_file, jsonify
from jinja2 import Template
import pdfkit
import os
import io

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("formulario.html")

@app.route("/generar", methods=["POST"])
def generar_pdf():
    # Recibir datos del formulario
    nombre = request.form.get("nombre")
    fecha = request.form.get("fecha")
    descripcion = request.form.get("descripcion")
    ruta_plantilla = os.path.join(os.path.dirname(__file__), "templates_pdf", "contrato.html")
    # Cargar plantilla de contrato
    with open( ruta_plantilla , "r") as f:
        template = Template(f.read())

    # Renderizar plantilla con datos del usuario
    html = template.render(nombre=nombre, fecha=fecha, descripcion=descripcion)

    # Especificar la ruta de wkhtmltopdf (si no está en el PATH)
    if os.name == 'nt':  # 'nt' es para Windows
        ruta_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
    else:
        ruta_wkhtmltopdf = "/usr/local/bin/wkhtmltopdf"
        
    config = pdfkit.configuration(wkhtmltopdf=ruta_wkhtmltopdf)

    # Convertir HTML a PDF
    pdf = pdfkit.from_string(html, False, configuration=config)

    # Enviar PDF al usuario como descarga
    return send_file(
        io.BytesIO(pdf),
        download_name="documento_generado.pdf",
        as_attachment=True,
    )

@app.errorhandler(500)
def internal_error(error):
    # Puedes registrar el error aquí, por ejemplo, en un archivo o base de datos
    app.logger.error(f"Error 500: {error}")
    return jsonify({"message": "Internal Server Error", "error": str(error)}), 500

if __name__ == "__main__":
    app.run(debug=True)
