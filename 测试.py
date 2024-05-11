import pymupdf

#识别pdf文件中的文字
pdf_document = pymupdf.open('./uploads/' + '发票实例_滴滴.pdf')

#识别pdf文件中的左上角1/4部分的文字
百分比=[0.073,0.7437,0.49670000000000003,0.0334]
text = "" 
for page in pdf_document:
    width=page.mediabox_size.x
    height=page.mediabox_size.y
    text += page.get_text("text", clip=[百分比[0]*width,百分比[1]*height,(百分比[2]+百分比[0])*width,(百分比[3]+百分比[1])*height]) 
print(text)
