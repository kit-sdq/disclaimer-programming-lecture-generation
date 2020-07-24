from flask import Flask
from flask import render_template
from flask import render_template_string
from flask import request
from pdfkit import from_string
from flask import make_response
from flask import redirect
from base64 import b64encode
from hashlib import sha256
from io import BytesIO
from json import dumps
import  qrcode
app = Flask(__name__)
@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/output', methods=['GET', 'POST'])
def form_result():
    if request.method == 'POST':
        return generate_pdf()
    return redirect("/")

def generate_pdf():

    # load output from html file
    with open('templates/pdf_template.html') as file:
        content = file.read()
    
    data = {}
    data['name'] = request.form.get("name")
    data['matricno'] = request.form.get("matricno")
    
    
    image_string = generate_qr_string(data)
    
    content = content.replace("%%name%%", data['name'])
    content = content.replace("%%matricno%%", data['matricno'] )
    content = content.replace("%%qr%%", image_string)
    pdf = from_string(content,False)
    
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = \
        'inline; filename=%s.pdf' % 'disclaimer'
    return response

def generate_qr_string(data):
    preHash = data['name'] + data['matricno']
    data['hash'] = sha256(preHash.encode("utf-8")).hexdigest()
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=0,
    )
    qr.add_data(dumps(data))
    qr.make(fit=True)
    image = qr.make_image(fill_color="black", back_color="white")

    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return b64encode(buffered.getvalue()).decode("utf-8")
