import cv2
from PIL import Image
from Modify_WH import Modify_WH
from Transparent_Pictures import Transparent_Pictures
from calculate_distance import Cal
from Scaling import Scaling

def Synthetic(image1,image2):
    
    haveface,havehair=Modify_WH('./data/Origin/Face/FacePicture.jpg','./data/Origin/Hair/HairPicture.jpg')

    if havehair==2 and haveface==0:
        composite_image1 = Image.open('./data/Pre-Process_2/incereaseW_image.png')
        or_image1 = './data/Pre-Process_2/incereaseW_image.png'
        composite_image2 = Image.open('./data/Origin/Face/FacePicture.jpg')
        or_image2 = './data/Origin/Face/FacePicture.jpg'
    elif haveface==2 and havehair==0:
        composite_image1 = Image.open('./data/Origin/Hair/HairPicture.jpg')
        or_image1 = './data/Origin/Hair/HairPicture.jpg'
        composite_image2 = Image.open('./data/Pre-Process_2/incereaseH_image.png')
        or_image2 = './data/Pre-Process_2/incereaseH_image.png'
    elif haveface==0 and havehair==1:
        composite_image1 = Image.open('./data/Origin/Face/FacePicture.jpg')
        or_image1 = './data/Origin/Face/FacePicture.jpg'
        composite_image1 = Image.open('./data/Pre-Process_2/incereaseW_image.png')
        or_image2 = './data/Pre-Process_2/incereaseW_image.png'
    elif haveface==1 and havehair==0:
        composite_image1 = Image.open('./data/Origin/Hair/HairPicture.jpg')
        or_image1 = './data/Origin/Hair/HairPicture.jpg'
        composite_image2 = Image.open('./data/Pre-Process_2/incereaseH_image.png')
        or_image2 = './data/Pre-Process_2/incereaseH_image.png'
    else:
        composite_image1 = Image.open('./data/Pre-Process_2/incereaseW_image.png')
        or_image1 = './data/Pre-Process_2/incereaseW_image.png'
        composite_image2 = Image.open('./data/Pre-Process_2/incereaseH_image.png')
        or_image2 = './data/Pre-Process_2/incereaseH_image.png'

    move_ratio_x,move_ratio_y = Cal(or_image1,or_image2)
    scale = Scaling(or_image1,or_image2)
    

    haveface,havehair=Modify_WH(image1,image2)
    Transparent_Pictures('./data/Pre-Process_2/incereaseH_image.png','./data/Pre-Process_2/transparent_face.png')
    Transparent_Pictures('./data/Pre-Process_2/incereaseW_image.png','./data/Pre-Process_2/transparent_hair.png')

    if havehair==2 and haveface==0:
        composite_image1 = Image.open('./data/Pre-Process_2/transparent_hair.png')
        or_image3 = './data/Pre-Process_2/transparent_hair.png'
        composite_image2 = Image.open('./data/Pre-Process_1/Face_matting.png')
    elif haveface==2 and havehair==0:
        composite_image1 = Image.open('./data/Pre-Process_1/Hair_matting.png')
        or_image3 = './data/Pre-Process_1/Hair_matting.png'
        composite_image2 = Image.open('./data/Pre-Process_2/transparent_face.png')
    elif haveface==0 and havehair==1:
        composite_image1 = Image.open('./data/Pre-Process_2/transparent_hair.png')
        or_image3 = './data/Pre-Process_2/transparent_hair.png'
        composite_image2 = Image.open('./data/Pre-Process_1/Face_matting.png')       
    elif haveface==1 and havehair==0:
        composite_image1 = Image.open('./data/Pre-Process_1/Hair_matting.png')
        or_image3 = './data/Pre-Process_1/Hair_matting.png'
        composite_image2 = Image.open('./data/Pre-Process_2/transparent_face.png')
    else:
        composite_image1 = Image.open('./data/Pre-Process_2/transparent_hair.png')
        or_image3 = './data/Pre-Process_2/transparent_hair.png'
        composite_image2 = Image.open('./data/Pre-Process_2/transparent_face.png')

    moved_width = int(composite_image2.width * move_ratio_x)
    moved_height = int(composite_image2.height * move_ratio_y)
    composite_image2 = composite_image2.crop((moved_width, moved_height, composite_image2.width, composite_image2.height))
    composite_image2.save('./data/Pre-Process_2/After_Face.png')

    haveface,havehair=Modify_WH(or_image3,'./data/Pre-Process_2/After_Face.png')
    Transparent_Pictures('./data/Pre-Process_2/incereaseH_image.png','./data/Pre-Process_2/transparent_face.png')
    Transparent_Pictures('./data/Pre-Process_2/incereaseW_image.png','./data/Pre-Process_2/transparent_hair.png')

    if havehair==2 and haveface==0:
        composite_image1 = Image.open('./data/Pre-Process_2/transparent_hair.png')
        composite_image2 = Image.open('./data/Pre-Process_2/After_Face.png')
    elif haveface==2 and havehair==0:
        composite_image1 = Image.open(or_image3)
        composite_image2 = Image.open('./data/Pre-Process_2/transparent_face.png')
    elif haveface==0 and havehair==1:
        composite_image1 = Image.open('./data/Pre-Process_2/transparent_hair.png')
        composite_image2 = Image.open('./data/Pre-Process_2/After_Face.png')       
    elif haveface==1 and havehair==0:
        composite_image1 = Image.open(or_image3)
        composite_image2 = Image.open('./data/Pre-Process_2/transparent_face.png')
    else:
        composite_image1 = Image.open('./data/Pre-Process_2/transparent_hair.png')
        composite_image2 = Image.open('./data/Pre-Process_2/transparent_face.png')

    # 使用Pillow的alpha_composite()方法合併
    merged_image = Image.alpha_composite(composite_image1.convert('RGBA'), composite_image2.convert('RGBA'))

    # 保存合併後的圖像
    merged_image.save('./data/Finish/finished_product.png')


if __name__=='__main__':
    image1 = './data/Pre-Process_1/Face_matting.png'
    image2 = './data/Pre-Process_1/Hair_matting.png'
    Synthetic(image1,image2)