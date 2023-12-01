from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import numpy as np
import matplotlib.pyplot as plt
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import numpy as np

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


def change():
    picture="./data/Origin/Face/FacePicture.jpg"
    dir=0
    x=[]
    y=[]
    base_options = python.BaseOptions(model_asset_path='face_landmarker_v2_with_blendshapes.task')
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

    #bot
    v1 = np.array([0, -10])
    v2 = np.array([x[1] * cutface.shape[1]-x[2] * cutface.shape[1], 
                   y[1] * cutface.shape[0]-y[2] * cutface.shape[0]])
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    cos_theta = dot_product / (norm_v1 * norm_v2)
    angle_in_radians = np.arccos(cos_theta)
    angle_in_degrees1 = np.degrees(angle_in_radians)
    

    #up
    v1 = np.array([0, 10])
    v2 = np.array([x[1] * cutface.shape[1]-x[168] * cutface.shape[1],
                   y[1] * cutface.shape[0]-y[168] * cutface.shape[0]])
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    cos_theta = dot_product / (norm_v1 * norm_v2)
    angle_in_radians = np.arccos(cos_theta)
    angle_in_degrees2 = np.degrees(angle_in_radians)
    

    #right
    v1 = np.array([10, 0])
    v2 = np.array([x[1] * cutface.shape[1]-x[205] * cutface.shape[1],
                   y[1] * cutface.shape[0]-y[205] * cutface.shape[0]])
    if y[1] * cutface.shape[0]-y[205] * cutface.shape[0] > 0 :
        dir = 1
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    cos_theta = dot_product / (norm_v1 * norm_v2)
    angle_in_radians = np.arccos(cos_theta)
    angle_in_degrees3 = np.degrees(angle_in_radians)
    

    #left
    v1 = np.array([-10, 0])
    v2 = np.array([x[1] * cutface.shape[1]-x[425] * cutface.shape[1],
                   y[1] * cutface.shape[0]-y[425] * cutface.shape[0]])
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    cos_theta = dot_product / (norm_v1 * norm_v2)
    angle_in_radians = np.arccos(cos_theta)
    angle_in_degrees4 = np.degrees(angle_in_radians)
    

    
    angle=(angle_in_degrees1+angle_in_degrees2+angle_in_degrees3+angle_in_degrees4)/4
    if angle > 15 :
        if dir == 1 :
            angle += 360.0
        elif dir ==0 :
            angle = 360.0 - angle
        return angle
    else :
        return 360.0

if __name__=="__main__":
    change()