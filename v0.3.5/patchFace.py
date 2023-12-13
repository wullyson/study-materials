import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
from FaceCorrection import change
from PIL import Image
from Feature_Point import Feature_point
from Transparent_Pictures import Transparent_Pictures

def haircut():
    # Create the options that will be used for ImageSegmenter
    base_options = python.BaseOptions(model_asset_path='selfie_multiclass_256x256.tflite')
    options = vision.ImageSegmenterOptions(base_options=base_options,
                                        output_category_mask=True)

    IMAGE_FILENAMES = ['./data/Pre-Process_5/8.jpg']
    # Create the image segmenter
    with vision.ImageSegmenter.create_from_options(options) as segmenter:

    # Loop through demo image(s)
        for image_file_name in IMAGE_FILENAMES:

            # Read the image using OpenCV
            original_image = cv2.imread(image_file_name)
            # Create the MediaPipe image file that will be segmented
            image = mp.Image.create_from_file(image_file_name)
            # Retrieve the masks for the segmented image
            segmentation_result = segmenter.segment(image)
            category_mask = segmentation_result.category_mask
            # Create a mask for hair region
            hair_mask = np.stack((category_mask.numpy_view()!=3,) * 3, axis=-1) > 0.2
            # Extract hair region from the original image
            
            hair_region = np.where(hair_mask, original_image, 0)

            hair_region = cv2.cvtColor(hair_region, cv2.COLOR_BGR2BGRA)
            gray=cv2.cvtColor(hair_region, cv2.COLOR_BGR2GRAY) 
            w=hair_region.shape[1]
            h=hair_region.shape[0]
            for x in range(w):
                for y in range(h):
                    if gray[y, x] == 0:
                        hair_region[y, x, 3] = 0 
            cv2.imwrite('./data/Pre-Process_7/Hair_matting.png',hair_region)

def pathch():
    picture="./data/Pre-Process_5/8.jpg"
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
    image = mp.Image.create_from_file(picture)
    # STEP 4: Detect face landmarks from the input image.
    detection_result = detector.detect(image)
    # STEP 5: Process the detection result. In this case, visualize it.

    cutface= cv2.imread(picture)

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
    cv2.imwrite('./data/Pre-Process_7/facetest.png', result)
    #合成
    composite_image1 = Image.open('./data/Pre-Process_7/facetest.png')
    composite_image2 = Image.open('./data/Pre-Process_7/Hair_matting.png')
    merged_image = Image.alpha_composite(composite_image1.convert('RGBA'), composite_image2.convert('RGBA'))
    merged_image.save('./data/Pre-Process_7/faceafter.png')

#比較圖片差異
    image1 = cv2.imread('./data/Pre-Process_7/faceafter.png')
    image2 = cv2.imread('./data/Pre-Process_5/8.jpg')
    # Convert images to grayscale
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # Compute absolute difference between the two images
    diff = cv2.absdiff(gray1, gray2)

    # Threshold the difference to create a binary mask
    _, pathchmask = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

    # Optionally, perform morphological operations to enhance the mask
    kernel = np.ones((5, 5), np.uint8)
    pathchmask = cv2.morphologyEx(pathchmask, cv2.MORPH_CLOSE, kernel)
    #cv2.cvtColor(pathchmask,cv2.COLOR_BAYER_BG2RGB)
    cv2.imwrite('./data/Pre-Process_7/mask.png', pathchmask)
#製作額頭顏色
    number=[6]
    getcolorimage = cv2.imread('./data/Origin/Face/FacePicture.jpg')
    pointX,pointY=Feature_point('./data/Origin/Face/FacePicture.jpg',number)
    pointX=int(pointX[0])
    pointY=int(pointY[0])

    width, height = 1,1
    roi = getcolorimage [pointY:pointY+height, pointX:pointX+width]
    # 计算该区域的平均颜色
    desired_color = np.mean(roi, axis=(0, 1)) # 这里使用 RGB 格式，你可以根据需要修改

    getcolorimage = cv2.imread('./data/Pre-Process_7/faceafter.png')

    rows, cols, _ = getcolorimage.shape

    # 创建一个和原图像相同大小的全零图像
    pathchResult = np.zeros((rows, cols, 3), dtype=np.uint8)

    # 获取遮罩区域的索引
    mask_indices = np.where(pathchmask > 0)
    pathchResult[mask_indices] = desired_color
    cv2.imwrite('./data/Pre-Process_7/patchImage.png',pathchResult)
    Transparent_Pictures('./data/Pre-Process_7/mask.png','./data/Pre-Process_7/mask.png')
    composite_image1 = Image.open('./data/Pre-Process_7/mask.png')
    composite_image2 = Image.open('./data/Pre-Process_7/faceafter.png')
    merged_image = Image.alpha_composite(composite_image2.convert('RGBA'), composite_image1.convert('RGBA'))
    merged_image.save('./data/Pre-Process_7/testpicture.png')

if __name__=='__main__':
    haircut() 
    pathch()   
    