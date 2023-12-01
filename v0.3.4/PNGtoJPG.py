from PIL import Image
import os

def convert_png_to_jpg(png_path, jpg_path, quality=95):
    # 打開PNG文件
    image = Image.open(png_path)
    
    # 如果圖像具有透明度通道，則將其轉換為RGB模式
    if image.mode == 'RGBA':
        image = image.convert('RGB')
    
    # 設置JPEG保存的質量（可選）
    # 默認值是95，你可以根據需要進行調整
    # 更高的值表示更高的質量，但文件大小更大
    image.save(jpg_path, 'JPEG', quality=quality)
