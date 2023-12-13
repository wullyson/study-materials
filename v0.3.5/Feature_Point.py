import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2

def Feature_point(picture,number):
    x=[]
    y=[]
    noisePointX=[]
    noisePointY=[]
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

    for i in number:
        noisePointX.append(x[i] * cutface.shape[1])
        noisePointY.append(y[i] * cutface.shape[0])
        
    return noisePointX,noisePointY

if __name__=="__main__":
    picture="./data/face/FacePicture.jpg"
    Feature_point(picture,1)