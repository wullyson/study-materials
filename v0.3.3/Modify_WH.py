import cv2
from PIL import Image
def incereaseW(width,image_input):
    
    # 获取原始图像的宽度和高度
    original_width, original_height = image_input.size

    # 设置要添加的宽度和高度
    additional_width = width  # 希望增加的宽度
    additional_height = 0  # 希望增加的高度

    # 计算新的宽度和高度
    new_width = original_width + additional_width
    new_height = original_height + additional_height

    # 创建一个新的黑色背景图像，尺寸为新的宽度和高度
    new_image = Image.new('RGB', (new_width, new_height), (0, 0, 0))

    # 将原始图像粘贴到新图像中央
    x_offset = (new_width - original_width) // 2
    y_offset = (new_height - original_height) // 2
    new_image.paste(image_input, (x_offset, y_offset))

    # 保存加宽或加高后的图像
    new_image.save('./data/Pre-Process_2/incereaseW_image.png')

def incereaseH(height,image_input):
    
    # 获取原始图像的宽度和高度
    original_width, original_height = image_input.size

    # 设置要添加的宽度和高度
    additional_width = 0  # 希望增加的宽度
    additional_height = height # 希望增加的高度

    # 计算新的宽度和高度
    new_width = original_width + additional_width
    new_height = original_height + additional_height

    # 创建一个新的黑色背景图像，尺寸为新的宽度和高度
    new_image = Image.new('RGB', (new_width, new_height), (0, 0, 0))

    # 将原始图像粘贴到新图像中央
    x_offset = (new_width - original_width) // 2
    y_offset = (new_height - original_height) // 2
    new_image.paste(image_input, (x_offset, y_offset))
    
    # 保存加宽或加高后的图像
    new_image.save('./data/Pre-Process_2/incereaseH_image.png')

def Modify_WH(FacePicture,HairPicture):
    image1 = cv2.imread(HairPicture)
    image1PIL=Image.open(HairPicture)
    image2 = cv2.imread(FacePicture)
    image2PIL=Image.open(FacePicture)
    Wgap=0
    Hgap=0
    haveface=0
    havehair=0
#改臉的長寬
    if image1.shape[1]>=image2.shape[1]:
        Wgap=image1.shape[1]-image2.shape[1]
        incereaseW(Wgap,image2PIL)
        image2=cv2.imread('./data/Pre-Process_2/incereaseW_image.png')
        image2PIL=Image.open("./data/Pre-Process_2/incereaseW_image.png")
        haveface=1
    
    if image1.shape[0]>=image2.shape[0]:
        Hgap=image1.shape[0]-image2.shape[0]
        incereaseH(Hgap,image2PIL)
        image2=cv2.imread('./data/Pre-Process_2/incereaseH_image.png')
        image2PIL=Image.open("./data/Pre-Process_2/incereaseH_image.png")
        haveface=2    
    
#改頭髮的長寬
    if image1.shape[0]<=image2.shape[0] and haveface!=2:
        Hgap=image2.shape[0]-image1.shape[0]
        incereaseH(Hgap,image1PIL)
        image1=cv2.imread('./data/Pre-Process_2/incereaseH_image.png')
        image1PIL=Image.open("./data/Pre-Process_2/incereaseH_image.png")
        havehair=1
    
    if image1.shape[1]<=image2.shape[1] and haveface!=1:
        Wgap=image2.shape[1]-image1.shape[1]
        incereaseW(Wgap,image1PIL)
        havehair=2
    
    return haveface,havehair

if __name__=='__main__':
    image1 = './data/Pre-Process_1/Face_matting.png'
    image2 = './data/Pre-Process_1/Hair_matting.png'
    Modify_WH(image1,image2)
   