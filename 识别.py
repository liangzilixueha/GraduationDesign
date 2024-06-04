import cv2
import pytesseract
from PIL import Image

# 如果需要，设置 tesseract 的路径
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# 读取图像
image = cv2.imread('output.jpg')
#二值化，非黑即白
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# 二值化处理
_, gray = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
#保存
cv2.imwrite('output_gray.jpg', gray)

# 识别文字
text = pytesseract.image_to_string(Image.open('output_gray.jpg'), lang='chi_sim')
print(text)

