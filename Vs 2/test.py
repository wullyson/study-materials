import numpy as np
import cv2
import torch
from facecut import facecut
from glob import glob
from PIL import Image
from torchvision import transforms
from nets.MobileNetV2_unet import MobileNetV2_unet
from convert import change
from receive import ReceivePicture
from host import SendPicture

# load pre-trained model and weights
def load_model():
    model = MobileNetV2_unet(None).to(args.device)
    state_dict = torch.load(args.pre_trained, map_location='cpu')
    model.load_state_dict(state_dict)
    model.eval()
    return model

def picture_Resize(new_w,new_h,image_throw):
    new_width = new_w
    new_height = new_h
    picture=image_throw
    # 计算宽度和高度的缩放比例
    width_ratio = new_width / picture.shape[1]
    height_ratio = new_height / picture.shape[0]

    # 选择较小的缩放比例，以确保图像适应新的宽度和高度
    min_ratio = min(width_ratio, height_ratio)

    # 计算新的宽度和高度
    new_width = int(picture.shape[1] * min_ratio)
    new_height = int(picture.shape[0] * min_ratio)

    # 调整图像的大小，并在周围填充空白
    resized_image = cv2.resize(picture, (new_width, new_height))
    resized_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2BGRA)
    gray_padded_image=cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY) 

    # # 将调整后的图像插入到具有透明背景的图像中
    for x in range(new_width):
        for y in range(new_height):
            if gray_padded_image[y, x] == 0:
                resized_image[y, x, 3] = 0 

    # 保存调整后的图像
    cv2.imwrite('./data/finish/FaceResize.png',resized_image)

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
    new_image.save('./data/finish/incereaseW_image.png')

    # 关闭图像对象
    image_input.close()
    new_image.close()

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
    new_image.save('./data/finish/incereaseH_image.png')

    # 关闭图像对象
    image_input.close()
    new_image.close()

if __name__ == '__main__':
    import argparse
    import matplotlib.pyplot as plt
    #接收傳送圖片
    ReceivePicture()

    parser = argparse.ArgumentParser(description='Semantic Segmentation')

    # Arguments
    parser.add_argument('--data-folder', type=str, default='./data/hair',
                        help='name of the data folder (default: ./data/hair)')
    parser.add_argument('--batch-size', type=int, default=1,
                        help='batch size (default: 8)')
    parser.add_argument('--pre-trained', type=str, default='./checkpoints/model.pt',
                        help='path of pre-trained weights (default: None)')

    args = parser.parse_args()
    args.device = torch.device("cpu")

    image_files = sorted(glob('{}/*.jp*g'.format(args.data_folder)))
    model = load_model()
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
    ])
    #print('Model loaded')
    print(len(image_files), ' files in folder ', args.data_folder)

    fig = plt.figure()
    for i, image_file in enumerate(image_files):
        if i >= args.batch_size:
            break

        oimage = cv2.imread(image_file)
        image = cv2.cvtColor(oimage, cv2.COLOR_BGR2RGB)

        pil_img = Image.fromarray(image)
        torch_img = transform(pil_img)
        torch_img = torch_img.unsqueeze(0)
        torch_img = torch_img.to(args.device)

        # Forward Pass
        logits = model(torch_img)
        mask = np.argmax(logits.data.cpu().numpy(), axis=1)
        
        # Plot
        ax = plt.subplot(2, args.batch_size, 2 * i + 1)
        ax.axis('off')
        ax.imshow(image.squeeze())

        ax = plt.subplot(2, args.batch_size, 2 * i + 2)
        ax.axis('off')
        ax.imshow(mask.squeeze())
        

    hair_mask = (mask.squeeze() == 2)
    
    hair_mask = cv2.resize(hair_mask.astype(np.uint8), (image.shape[1], image.shape[0]))
    hair_image = np.zeros_like(image)
    hair_image[hair_mask > 0] = oimage[hair_mask > 0]

    hair_image = cv2.cvtColor(hair_image, cv2.COLOR_BGR2BGRA)
    gray=cv2.cvtColor(hair_image, cv2.COLOR_BGR2GRAY) 
    w=hair_image.shape[1]
    h=hair_image.shape[0]
    for x in range(w):
        for y in range(h):
            if gray[y, x] == 0:
                hair_image[y, x, 3] = 0 
    
# 儲存頭髮去背圖片
    cv2.imwrite('./data/finish/hair_part.png', hair_image)
# 顯示頭髮切割部分
    #cv2.imshow('Hair Part', hair_image)
    #cv2.waitKey(0)
#顯示臉部
    facecut()

image = Image.open('./data/finish/output_face.png')
rotated_image = image.rotate(change())
rotated_image.save('./data/finish/rotated_image.png')
# 显示旋转后的图像
#rotated_image.show()

# 打开第一张图像
image1 = cv2.imread("./data/finish/hair_part.png")
image1PIL=Image.open("./data/finish/hair_part.png")
# 打开第二张图像
image2 = cv2.imread('./data/finish/rotated_image.png')
image2PIL=Image.open("./data/finish/rotated_image.png")
Wgap=0
Hgap=0
have=0
# 设置新的照片大小
if image1.shape[1]>image2.shape[1]:
    Wgap=image1.shape[1]-image2.shape[1]
    incereaseW(Wgap,image2PIL)
    have=1
if image1.shape[0]>image2.shape[0]:
    Hgap=image1.shape[0]-image2.shape[0]
    incereaseH(Hgap,image2PIL)
    have=2

if have==1:
    image2_2 = cv2.imread('./data/finish/incereaseW_image.png')
    image2_2PIL = Image.open('./data/finish/incereaseW_image.png')
elif have==2:
    image2_2 = cv2.imread('./data/finish/incereaseH_image.png')
    image2_2PIL = Image.open('./data/finish/incereaseH_image.png')
else:
    image2_2 = cv2.imread('./data/finish/rotated_image.png')  
    image2_2PIL = Image.open('./data/finish/rotated_image.png')

if image1.shape[0]<image2_2.shape[0]:
    Hgap=image2_2.shape[0]-image1.shape[0]
    incereaseH(Hgap,image1PIL)
if image1.shape[1]<image2_2.shape[1]:
    Wgap=image2_2.shape[1]-image1.shape[1]
    incereaseW(Wgap,image1PIL)

transparent_image1=cv2.imread('./data/finish/incereaseH_image.png')
transparent_image1 = cv2.cvtColor(transparent_image1, cv2.COLOR_BGR2BGRA)
gray_transparent_image1=cv2.cvtColor(transparent_image1, cv2.COLOR_BGR2GRAY) 
w=transparent_image1.shape[1]
h=transparent_image1.shape[0]
for x in range(w):
    for y in range(h):
        if gray_transparent_image1[y, x] == 0:
            transparent_image1[y, x, 3] = 0 
cv2.imwrite('./data/finish/transparent_face.png',transparent_image1)

transparent_image2=cv2.imread('./data/finish/incereaseW_image.png')
transparent_image2 = cv2.cvtColor(transparent_image2, cv2.COLOR_BGR2BGRA)
gray_transparent_image2=cv2.cvtColor(transparent_image2, cv2.COLOR_BGR2GRAY) 
w=transparent_image2.shape[1]
h=transparent_image2.shape[0]
for x in range(w):
    for y in range(h):
        if gray_transparent_image2[y, x] == 0:
            transparent_image2[y, x, 3] = 0 
cv2.imwrite('./data/finish/transparent_hair.png',transparent_image2) 

# 设置新的宽度和高度
#picture_Resize(image1.shape[1],image1.shape[0],image2)


composite_image1 = Image.open('./data/finish/transparent_hair.png')
composite_image2 = Image.open('./data/finish/transparent_face.png')
#if composite_image1.size != composite_image2.size:
    #composite_image2 = composite_image2.resize(composite_image1.size)
# 使用Pillow的alpha_composite()方法将两张图像合并，考虑透明度
merged_image = Image.alpha_composite(composite_image2.convert('RGBA'), composite_image1.convert('RGBA'))

# 保存合并后的图像
merged_image.save('./data/done/after.png')

#發送圖片
SendPicture()
# 显示合并后的图像
#merged_image.show()


