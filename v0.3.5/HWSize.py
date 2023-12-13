from Feature_Point import Feature_point
import cv2
import numpy as np
# 读取图像
number=[6]
getcolorimage = cv2.imread('./data/Origin/Face/FacePicture.jpg')
pointX,pointY=Feature_point('./data/Origin/Face/FacePicture.jpg',number)
pointX=int(pointX[0])
pointY=int(pointY[0])

width, height = 1,1
roi = getcolorimage [pointY:pointY+height, pointX:pointX+width]

# 计算该区域的平均颜色
average_color = np.mean(roi, axis=(0, 1))

print(f'Average Color in the specified region: {average_color}')
