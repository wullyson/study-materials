from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import numpy as np
import matplotlib.pyplot as plt
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
diff_left_x = 0.0
diff_left_y = 0.0
diff_right_x = 0.0
diff_right_y = 0.0
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

def Noise_Feature_point_Left(picture):
    global diff_left_x
    global diff_left_y
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
    cutface= cv2.imread(picture)
    """We will also visualize the face blendshapes categories using a bar graph."""
    #plot_face_blendshapes_bar_graph(detection_result.face_blendshapes[0])
    for landmark in detection_result.face_landmarks[0]:
        x.append(landmark.x)
        y.append(landmark.y)
    
    LeftPointX=x[123] * cutface.shape[1]
    LeftPointY=y[123] * cutface.shape[0]

    diff_left_x = LeftPointX - diff_left_x
    diff_left_y = LeftPointY - diff_left_y
    
def Noise_Feature_point_Right(picture):
    global diff_right_x
    global diff_right_y
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
    cutface= cv2.imread(picture)
    """We will also visualize the face blendshapes categories using a bar graph."""
    #plot_face_blendshapes_bar_graph(detection_result.face_blendshapes[0])
    for landmark in detection_result.face_landmarks[0]:
        x.append(landmark.x)
        y.append(landmark.y)
    
    RightPointX=x[352] * cutface.shape[1]
    RightPointY=y[352] * cutface.shape[0]

    diff_right_x = RightPointX - diff_right_x
    diff_right_y = RightPointY - diff_right_y
def Picture_wh(picture):
    img = cv2.imread(picture)
    img_height, img_width, _ = img.shape 
    
    return img_width, img_height  

def Scaling(image1,image2):
    Noise_Feature_point_Left(image1)
    Noise_Feature_point_Right(image1)

    Noise_Feature_point_Left(image2)
    Noise_Feature_point_Right(image2)
    img_width, img_height = Picture_wh(image1)
    range_width = img_width /100
    range_height = img_width /100
    if ( -range_width < diff_left_x <=0 and -range_width < diff_right_x <=0) or (range_width > diff_left_x >=0 and range_width > diff_right_x >=0):
        avg_total = 100
        
    elif ( diff_left_x <=0 and diff_right_x >=0 ): #臉縮小
        dis_left_x = diff_left_x / img_width
        dis_right_x = diff_right_x / img_width
        print(dis_left_x,dis_right_x)
        avg_total = (abs(dis_left_x) + abs(dis_right_x)) / 2.0 * 100
        
    elif ( diff_left_x >=0 and diff_right_x <=0) : #臉放大
        dis_left_x = diff_left_x / img_width
        dis_right_x = diff_right_x / img_width
        avg_total = (abs(dis_left_x) + abs(dis_right_x)) / 2.0 * 100
        avg_total = 80 - avg_total
    else :
        avg_total = 100
    return avg_total
 
if __name__=="__main__":
    Scaling()