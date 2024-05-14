import json
import os
import sqlite3
from flask import Blueprint, jsonify, redirect, render_template, request, send_file, url_for
from PIL import Image
import pytesseract
import pymupdf

from WebPy.data import DataBase

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

@paper.route('/ocr', methods=['POST'])
def get_pdf_text():
    #获取前端body中的json数据
    data = request.get_data()
    data = json.loads(data)
    print(data)
    #识别pdf文件中的文字
    pdf_document = pymupdf.open('./uploads/' + data['filename'])
    text = "" 
    for page in pdf_document:
        width=page.mediabox_size.x
        height=page.mediabox_size.y
        text += page.get_text("text", clip=
                              [data['x']*width,
                                 data['y']*height,
                                 (data['dx']+data['x'])*width,
                                 (data['dy']+data['y'])*height])
    return text

@paper.route('/save', methods=['POST'])
def save():
    #接受前端传来的json数据
    data = request.get_data()
    #输出文件名
    json_data = json.loads(data.decode('utf-8'))
    print(json_data['filename'])
    json_data['filename'] = json_data['filename'].split('.')[0]
    #输出文件内容
    maindata=json_data['data']
    db=DataBase(json_data['filename'])
    t=[]
    for key in maindata:
        j={
        "name":key[0],
        "x":key[1],
        "y":key[2],
        "dx":key[3],
        "dy":key[4],
        "ocr":key[5]
        }
        t.append(j)
    #把t变成json格式
    t=json.dumps(t)
    db.insert(json_data['filename'],t)
    db.close()
    return 'success',200

@paper.route('/db/get_all', methods=['GET'])
def get_all():
    #获取/db/get_all后?的table_name
    table_name = request.args.get('table_name')
    if(table_name is None):
        db = sqlite3.connect('data.db')
        cursor = db.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        db.commit()
        tables = cursor.fetchall()
        db.close()
        return jsonify(tables)
    db=DataBase(table_name)
    data=db.select()
    json=jsonify(data)
    print(json)
    db.close()
    return json

@paper.route('/db', methods=['GET'])
def db():
    return render_template('database.html')

#使用纯种的OCR而不是pdf识别
@paper.route('/ocr-low', methods=['POST'])
def ocr_low():
    #获取前端传来的json数据
    data = request.get_data()
    #输出文件名
    json_data = json.loads(data.decode('utf-8'))
    print(json_data['filename'])
    x=json_data['x']
    y=json_data['y']
    dx=json_data['dx']
    dy=json_data['dy']
    #使用OCR在区域内识别文字
    img=Image.open('./uploads/' + json_data['filename'])
    width,height=img.size
    img=img.crop((x*width,y*height,(x+dx)*width,(y+dy)*height))
    text = pytesseract.image_to_string(image=img,lang='chi_sim')
    return text