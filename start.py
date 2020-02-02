from flask import Flask
from flask import render_template
import  qrcode
app = Flask(__name__)
@app.route('/')
def hello_world():
    return render_template('index.html')
@app.route('disclaimer/output')
def generate_pdf():
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants,ERROR_CORRECT_H
        box_size=10,
        border=4,
    )
    qr.add_data('test')
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")