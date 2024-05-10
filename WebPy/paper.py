import os
from flask import Blueprint, jsonify, redirect, render_template, request, send_file, url_for
from PIL import Image
import pytesseract
import pymupdf

paper=Blueprint('paper',__name__)

@paper.route('/')
def index():
    return render_template('index.html')

@paper.route('/mark')
def red():
    return render_template('mark.html')

@paper.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return redirect(request.url)
    
    file = request.files['image']
    if file.filename == '':
        return redirect(request.url)
    
    if file:
        filename = file.filename
        filepath = os.path.join('uploads', filename)
        file.save(filepath)
        text = pytesseract.image_to_string(Image.open(filepath),lang='chi_sim')
        return text
    
@paper.route('/uploadpdf', methods=['POST'])
def upload_pdf():
    # 获取前端上传的文件
    file = request.files['file']
    # 保存文件
    file.save('uploads/' + file.filename)
    # 将pdf的第一页转换为图片
    pdf_document = pymupdf.open('uploads/' + file.filename)
    first_page = pdf_document[0]
    pix = first_page.get_pixmap(matrix=pymupdf.Matrix(2, 2))
    image_path = 'uploads/first_page.png'
    pix.save(image_path)  # 保存图片
    pdf_document.close()  # 关闭PDF
    return send_file(image_path, mimetype='image/png')