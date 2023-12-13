import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
from FaceCorrection import change
from PIL import Image


def facecut():
    picture="./data/Origin/Face/FacePicture.jpg"
    face_points=[]
    index=[
        10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288,
        397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136,
        172, 58, 132, 93, 234, 127, 162, 21, 54, 103, 67, 109
    ]
    x=[]
    y=[]
    base_options = python.BaseOptions(model_asset_path='./face_landmarker_v2_with_blendshapes.task')
    options = vision.FaceLandmarkerOptions(base_options=base_options,
                                        output_face_blendshapes=True,
                                        output_facial_transformation_matrixes=True,
                                        num_faces=1)
    detector = vision.FaceLandmarker.create_from_options(options)
    # STEP 3: Load the input image.
    image = mp.Image.create_from_file(picture)
    # STEP 4: Detect face landmarks from the input image.
    detection_result = detector.detect(image)
    # STEP 5: Process the detection result. In this case, visualize it.

    cutface= cv2.imread(picture)
    """We will also visualize the face blendshapes categories using a bar graph."""
    #plot_face_blendshapes_bar_graph(detection_result.face_blendshapes[0])
    for landmark in detection_result.face_landmarks[0]:
            x.append(landmark.x)
            y.append(landmark.y)
    for i in index:
        face_points.append((x[i] * cutface.shape[1],y[i] * cutface.shape[0]))

    mask = np.zeros_like(cutface)

# 使用特徵點座標创建一个輪廓
    contour = np.array(face_points, dtype=np.int32)
    cv2.fillPoly(mask, [contour], (255, 255, 255))

# 将掩码应用于输入图像以提取輪廓区域
    result = cv2.bitwise_and(cutface, mask)
# 將臉部轉正    
    image = Image.fromarray(result)
    result = image.rotate(change())
    result = np.array(result)
# 將背景轉透明
    result = cv2.cvtColor(result, cv2.COLOR_BGR2BGRA)
    gray=cv2.cvtColor(result, cv2.COLOR_BGR2GRAY) 
    w=result.shape[1]
    h=result.shape[0]
    for x in range(w):
        for y in range(h):
            if gray[y, x] == 0:
                result[y, x, 3] = 0 
# 儲存臉部去背圖片
    cv2.imwrite('./data/Pre-Process_1/Face_matting.png', result)

if __name__=="__main__":
    facecut()