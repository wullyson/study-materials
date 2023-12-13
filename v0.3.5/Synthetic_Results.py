import cv2
from PIL import Image
from Modify_WH import Modify_WH
from calculate_distance import Cal
from Scaling import Scaling
from Resize import resize_image
from PNGtoJPG import convert_png_to_jpg

def Synthetic(image1,image2):
    
    haveface,havehair=Modify_WH('./data/Origin/Face/FacePicture.jpg','./data/Origin/Hair/HairPicture.jpg',
                                './data/Pre-Process_2/increaseW_Face.jpg','./data/Pre-Process_2/increaseH_Face.jpg',
                                './data/Pre-Process_2/increaseW_Hair.jpg','./data/Pre-Process_2/increaseH_Hair.jpg')
    if haveface==3 and havehair==0:
        composite_image1 = Image.open('./data/Pre-Process_2/increaseH_Face.jpg')
        or_image1 = './data/Pre-Process_2/increaseH_Face.jpg'
        composite_image2 = Image.open('./data/Origin/Hair/HairPicture.jpg')
        or_image2 = './data/Origin/Hair/HairPicture.jpg'
        
    elif havehair==3 and haveface==0:
        composite_image1 = Image.open('./data/Origin/Face/FacePicture.jpg')
        or_image1 = './data/Origin/Face/FacePicture.jpg'
        composite_image2 = Image.open('./data/Pre-Process_2/increaseH_Hair.jpg')
        or_image2 = './data/Pre-Process_2/increaseH_Hair.jpg'
    elif haveface==2 and havehair==1:
        composite_image1 = Image.open('./data/Pre-Process_2/increaseH_Face.jpg')
        or_image1 = './data/Pre-Process_2/increaseH_Face.jpg'
        composite_image2 = Image.open('./data/Pre-Process_2/increaseW_Hair.jpg')
        or_image2 = './data/Pre-Process_2/increaseW_Hair.jpg'
    elif haveface==1 and havehair==2:
        composite_image1 = Image.open('./data/Pre-Process_2/increaseW_Face.jpg')
        or_image1 = './data/Pre-Process_2/increaseW_Face.jpg'
        composite_image2 = Image.open('./data/Pre-Process_2/increaseH_Hair.jpg')
        or_image2 = './data/Pre-Process_2/increaseH_Hair.jpg'
    else:
        composite_image1 = Image.open('./data/Origin/Face/FacePicture.jpg')
        or_image1 = './data/Origin/Face/FacePicture.jpg'
        composite_image2 = Image.open('./data/Origin/Hair/HairPicture.jpg')
        or_image2 = './data/Origin/Hair/HairPicture.jpg'

    move_ratio_x,move_ratio_y = Cal(or_image1,or_image2)
    
    
    haveface,havehair=Modify_WH(image1,image2,
                                './data/Pre-Process_3/increaseW_Face.png','./data/Pre-Process_3/increaseH_Face.png',
                                './data/Pre-Process_3/increaseW_Hair.png','./data/Pre-Process_3/increaseH_Hair.png')
    if haveface==3 and havehair==0:
        composite_image1 = Image.open('./data/Pre-Process_3/increaseH_Face.png')
        or_image3 = './data/Pre-Process_3/increaseH_Face.png'
        composite_image2 = Image.open(image2)
        or_image4 = image2
    elif havehair==3 and haveface==0:
        composite_image1 = Image.open(image1)
        or_image3 = image1
        composite_image2 = Image.open('./data/Pre-Process_3/increaseH_Hair.png')
        or_image4 = './data/Pre-Process_3/increaseH_Hair.png'
    elif haveface==2 and havehair==1:
        composite_image1 = Image.open('./data/Pre-Process_3/increaseH_Face.png')
        or_image3 = './data/Pre-Process_3/increaseH_Face.png'
        composite_image2 = Image.open('./data/Pre-Process_3/increaseW_Hair.png')
        or_image4 = './data/Pre-Process_3/increaseW_Hair.png'
    elif haveface==1 and havehair==2:
        composite_image1 = Image.open('./data/Pre-Process_3/increaseW_Face.png')
        or_image3 = './data/Pre-Process_3/increaseW_Face.png'
        composite_image2 = Image.open('./data/Pre-Process_3/increaseH_Hair.png')
        or_image4 = './data/Pre-Process_3/increaseH_Hair.png'
    else:
        composite_image1 = Image.open(image1)
        or_image3 = image1
        composite_image2 = Image.open(image2)
        or_image4 = image2


    moved_width = int(composite_image1.width * move_ratio_x)
    moved_height = int(composite_image1.height * move_ratio_y)
    composite_image1 = composite_image1.crop((moved_width, moved_height, composite_image2.width, composite_image2.height))
    composite_image1.save('./data/Pre-Process_3/After_Cal.png')
    or_image3 = './data/Pre-Process_3/After_Cal.png'
    haveface,havehair=Modify_WH(or_image3,or_image4,
                                './data/Pre-Process_4/increaseW_Face.png','./data/Pre-Process_4/increaseH_Face.png',
                                './data/Pre-Process_4/increaseW_Hair.png','./data/Pre-Process_4/increaseH_Hair.png')
    if haveface==3 and havehair==0:
        composite_image1 = Image.open('./data/Pre-Process_4/increaseH_Face.png')
        or_image5 = './data/Pre-Process_4/increaseH_Face.png'
        composite_image2 = Image.open(or_image4)
        or_image6 = or_image4
    elif havehair==3 and haveface==0:
        composite_image1 = Image.open(or_image3)
        or_image5 = or_image3
        composite_image2 = Image.open('./data/Pre-Process_4/increaseH_Hair.png')
        or_image6 = './data/Pre-Process_4/increaseH_Hair.png'
    elif haveface==2 and havehair==1:
        composite_image1 = Image.open('./data/Pre-Process_4/increaseH_Face.png')
        or_image5 = './data/Pre-Process_4/increaseH_Face.png'
        composite_image2 = Image.open('./data/Pre-Process_4/increaseW_Hair.png')
        or_image6 = './data/Pre-Process_4/increaseW_Hair.png'
    elif haveface==1 and havehair==2:
        composite_image1 = Image.open('./data/Pre-Process_4/increaseW_Face.png')
        or_image5 = './data/Pre-Process_4/increaseW_Face.png'
        composite_image2 = Image.open('./data/Pre-Process_4/increaseH_Hair.png')
        or_image6 = './data/Pre-Process_4/increaseH_Hair.png'
    else:
        composite_image1 = Image.open(or_image3)
        or_image5 = or_image3
        composite_image2 = Image.open(or_image4)
        or_image6 = or_image4

    haveface,havehair=Modify_WH(or_image5,'./data/Origin/Hair/HairPicture.jpg',
                                './data/Pre-Process_5/increaseW_Face.png','./data/Pre-Process_5/increaseH_Face.png',
                                './data/Pre-Process_5/increaseW_Hair.png','./data/Pre-Process_5/increaseH_Hair.png')

    if haveface==3 and havehair==0:
        composite_image1 = Image.open('./data/Pre-Process_5/increaseH_Face.png')
        or_image7 = './data/Pre-Process_5/increaseH_Face.png'
        composite_image2 = Image.open('./data/Origin/Hair/HairPicture.jpg')
        or_image8 = './data/Origin/Hair/HairPicture.jpg'
    elif havehair==3 and haveface==0:
        composite_image1 = Image.open(or_image5)
        or_image7 = or_image5
        composite_image2 = Image.open('./data/Pre-Process_5/increaseH_Hair.png')
        or_image8 = './data/Pre-Process_5/increaseH_Hair.png'
    elif haveface==2 and havehair==1:
        composite_image1 = Image.open('./data/Pre-Process_5/increaseH_Face.png')
        or_image7 = './data/Pre-Process_5/increaseH_Face.png'
        composite_image2 = Image.open('./data/Pre-Process_5/increaseW_Hair.png')
        or_image8 = './data/Pre-Process_5/increaseW_Hair.png'
    elif haveface==1 and havehair==2:
        composite_image1 = Image.open('./data/Pre-Process_5/increaseW_Face.png')
        or_image7 = './data/Pre-Process_5/increaseW_Face.png'
        composite_image2 = Image.open('./data/Pre-Process_5/increaseH_Hair.png')
        or_image8 = './data/Pre-Process_5/increaseH_Hair.png'
    else:
        composite_image1 = Image.open(or_image5)
        or_image7 = or_image5
        composite_image2 = Image.open('./data/Origin/Hair/HairPicture.jpg')
        or_image8 = './data/Origin/Hair/HairPicture.jpg'

    convert_png_to_jpg(or_image7,'./data/Pre-Process_5/7.jpg')
    convert_png_to_jpg(or_image8,'./data/Pre-Process_5/8.jpg')
    scale = Scaling('./data/Pre-Process_5/7.jpg','./data/Pre-Process_5/8.jpg')
    resize_image('./data/Pre-Process_5/7.jpg',scale)
    or_image7 = './data/Pre-Process_5/After_Resize.png'

    haveface,havehair=Modify_WH(or_image7,or_image6,
                                './data/Pre-Process_6/increaseW_Face.png','./data/Pre-Process_6/increaseH_Face.png',
                                './data/Pre-Process_6/increaseW_Hair.png','./data/Pre-Process_6/increaseH_Hair.png')

    if haveface==3 and havehair==0:
        composite_image1 = Image.open('./data/Pre-Process_6/increaseH_Face.png')
        composite_image2 = Image.open(or_image6)
    elif havehair==3 and haveface==0:
        composite_image1 = Image.open(or_image7)
        composite_image2 = Image.open('./data/Pre-Process_6/increaseH_Hair.png')
    elif haveface==2 and havehair==1:
        composite_image1 = Image.open('./data/Pre-Process_6/increaseH_Face.png')
        composite_image2 = Image.open('./data/Pre-Process_6/increaseW_Hair.png')
    elif haveface==1 and havehair==2:
        composite_image1 = Image.open('./data/Pre-Process_6/increaseW_Face.png')
        composite_image2 = Image.open('./data/Pre-Process_6/increaseH_Hair.png')
    else:
        composite_image1 = Image.open(or_image7)
        composite_image2 = Image.open(or_image6)

    # 使用Pillow的alpha_composite()方法合併
    merged_image = Image.alpha_composite(composite_image1.convert('RGBA'), composite_image2.convert('RGBA'))

    # # 保存合併後的圖像
    merged_image.save('./data/Finish/Final.png')


if __name__=='__main__':
    image1 = './data/Pre-Process_1/Face_matting.png'
    image2 = './data/Pre-Process_1/Hair_matting.png'
    Synthetic(image1,image2)