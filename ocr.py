import cv2
import numpy as np
from PIL import Image

def rotate_image(image, angle):
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)

    # 旋转矩阵
    M = cv2.getRotationMatrix2D((cX, cY), angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    # 计算新边界尺寸
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))

    # 调整旋转矩阵的平移部分
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY

    # 执行实际旋转和缩放
    return cv2.warpAffine(image, M, (nW, nH))

def 画出文字区域(image, boxes):
    for box in boxes:
        box = box.astype(np.int32)
        cv2.polylines(image, [box], True, (0, 255, 0), 2)
    return image

# 读取图像
image = cv2.imread('img2.png')

# 转为灰度图像
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 边缘检测
edged = cv2.Canny(gray, 50, 150)

# 查找轮廓
contours, _ = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

# 找到最大轮廓
largest_contour = max(contours, key=cv2.contourArea)
# 画出最大轮廓
cv2.drawContours(image, [largest_contour], -1, (0, 255, 0), 2)

# 获取最小外接矩形
rect = cv2.minAreaRect(largest_contour)
#画出最小外接矩形
box = cv2.boxPoints(rect)
box = np.int0(box)
cv2.drawContours(image, [box], 0, (0, 0, 255), 2)

angle = rect[-1]

# 调整角度范围
if angle < -45:
    angle = -(90 + angle)
else:
    angle = -angle

# 旋转图像
rotated = rotate_image(image, angle+90)


# 保存旋转后的图像
cv2.imwrite('output.jpg', rotated)



