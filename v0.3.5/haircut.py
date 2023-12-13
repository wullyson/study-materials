import numpy as np
import mediapipe as mp
import cv2
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

def haircut():
    # Create the options that will be used for ImageSegmenter
    base_options = python.BaseOptions(model_asset_path='selfie_multiclass_256x256.tflite')
    options = vision.ImageSegmenterOptions(base_options=base_options,
                                        output_category_mask=True)

    IMAGE_FILENAMES = ['./data/Origin/Hair/HairPicture.jpg']
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
            hair_mask = np.stack((category_mask.numpy_view()==1,) * 3, axis=-1) > 0.2
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
            cv2.imwrite('./data/Pre-Process_1/Hair_matting.png',hair_region)

if __name__=="__main__":
    haircut()