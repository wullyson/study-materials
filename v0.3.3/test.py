import cv2

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

    return resized_img
if __name__=="__main__":
    resize_image()



