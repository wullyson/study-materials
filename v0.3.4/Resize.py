import cv2
from Transparent_Pictures import Transparent_Pictures

def resize_image(image_path, scale_percent):
    # 讀取圖像
    img = cv2.imread(image_path)

    # 獲取圖像的寬度和高度
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    # 設置新的寬度和高度
    new_dim = (width, height)

    # 使用resize函數進行縮放
    resized_img = cv2.resize(img, new_dim, interpolation=cv2.INTER_AREA)

    cv2.imwrite('./data/Pre-Process_5/After_Resize.png', resized_img)

    Transparent_Pictures('./data/Pre-Process_5/After_Resize.png','./data/Pre-Process_5/After_Resize.png')

if __name__=="__main__":
    resize_image()



