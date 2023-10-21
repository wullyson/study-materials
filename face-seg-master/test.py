import numpy as np
import cv2
import torch

from facecut import facecut
from glob import glob
from PIL import Image
from torchvision import transforms
from nets.MobileNetV2_unet import MobileNetV2_unet
from convert import change


# load pre-trained model and weights
def load_model():
    model = MobileNetV2_unet(None).to(args.device)
    state_dict = torch.load(args.pre_trained, map_location='cpu')
    model.load_state_dict(state_dict)
    model.eval()
    return model


if __name__ == '__main__':
    import argparse
    import matplotlib.pyplot as plt

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
    print('Model loaded')
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
rotated_image = image.rotate(360.0-change())
rotated_image.save('./data/finish/rotated_image.png')
# 显示旋转后的图像
#rotated_image.show()

# 打开第一张图像
image1 = Image.open("./data/finish/hair_part.png")

# 打开第二张图像
image2 = Image.open("./data/finish/rotated_image.png")

# 获取两张图像的原始宽度和高度
width1, height1 = image1.size
width2, height2 = image2.size

# 计算两张图像的宽高比例
aspect_ratio1 = width1 / height1
aspect_ratio2 = width2 / height2

# 确定新图像的目标宽度
new_width = min(width1, width2)
new_height1 = int(new_width / aspect_ratio1)
new_height2 = int(new_width / aspect_ratio2)

# 裁剪和调整第一张图像的大小
image1 = image1.resize((new_width, new_height1), Image.Resampling.LANCZOS)
# 裁剪和调整第二张图像的大小
image2 = image2.resize((new_width, new_height2), Image.Resampling.LANCZOS)

# 现在，image1和image2都具有相同的比例，可以进一步处理或显示它们
#image1.show()
#image2.show()

# 保存处理后的图像
image1.save("image1_resized.png")
image2.save("image2_resized.png")

image1 = Image.open('image1_resized.png')
image2 = Image.open('image2_resized.png')

# 确保两张图像的大小相同，如果不同，可以使用resize()方法调整它们
if image2.size != image1.size:
    image2 = image2.resize(image1.size)
# 使用Pillow的alpha_composite()方法将两张图像合并，考虑透明度
merged_image = Image.alpha_composite(image2.convert('RGBA'), image1.convert('RGBA'))

# 保存合并后的图像
merged_image.save('./data/done/after.png')

# 显示合并后的图像
merged_image.show()


