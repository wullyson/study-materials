from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import numpy as np
import matplotlib.pyplot as plt
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
from FaceCorrection import change
from PIL import Image

def draw_landmarks_on_image(rgb_image, detection_result):
    face_landmarks_list = detection_result.face_landmarks
    annotated_image = np.copy(rgb_image)

    # Loop through the detected faces to visualize.
    for idx in range(len(face_landmarks_list)):
        face_landmarks = face_landmarks_list[idx]

        # Draw the face landmarks.
        face_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        face_landmarks_proto.landmark.extend([
            landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in face_landmarks
        ])

        solutions.drawing_utils.draw_landmarks(
                image=annotated_image,
                landmark_list=face_landmarks_proto,
                connections=mp.solutions.face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp.solutions.drawing_styles
                .get_default_face_mesh_tesselation_style())
        solutions.drawing_utils.draw_landmarks(
                image=annotated_image,
                landmark_list=face_landmarks_proto,
                connections=mp.solutions.face_mesh.FACEMESH_CONTOURS,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp.solutions.drawing_styles
                .get_default_face_mesh_contours_style())
        solutions.drawing_utils.draw_landmarks(
                image=annotated_image,
                landmark_list=face_landmarks_proto,
                connections=mp.solutions.face_mesh.FACEMESH_IRISES,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp.solutions.drawing_styles
                    .get_default_face_mesh_iris_connections_style())
    
    return annotated_image
        
def plot_face_blendshapes_bar_graph(face_blendshapes):
    # Extract the face blendshapes category names and scores.
    face_blendshapes_names = [face_blendshapes_category.category_name for face_blendshapes_category in face_blendshapes]
    face_blendshapes_scores = [face_blendshapes_category.score for face_blendshapes_category in face_blendshapes]
    # The blendshapes are ordered in decreasing score value.
    face_blendshapes_ranks = range(len(face_blendshapes_names))

    fig, ax = plt.subplots(figsize=(12, 12))
    bar = ax.barh(face_blendshapes_ranks, face_blendshapes_scores, label=[str(x) for x in face_blendshapes_ranks])
    ax.set_yticks(face_blendshapes_ranks, face_blendshapes_names)
    ax.invert_yaxis()

    # Label each bar with values
    for score, patch in zip(face_blendshapes_scores, bar.patches):
        plt.text(patch.get_x() + patch.get_width(), patch.get_y(), f"{score:.4f}", va="top")

    ax.set_xlabel('Score')
    ax.set_title("Face Blendshapes")
    plt.tight_layout()
    plt.show()


def facecut():
    picture="./data/face/FacePicture.jpg"
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
    annotated_image = draw_landmarks_on_image(image.numpy_view(), detection_result)
    #cv2.imshow("ASM",cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR))
    #cv2.waitKey(0)
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
    cv2.imwrite('./data/finish/output_face.png', result)

if __name__=="__main__":
    facecut()