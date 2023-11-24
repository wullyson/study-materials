import numpy as np
import cv2
import torch
from glob import glob
from PIL import Image
from torchvision import transforms
from nets.MobileNetV2_unet import MobileNetV2_unet

# load pre-trained model and weights
def load_model(args):
    model = MobileNetV2_unet(None).to(args.device)
    state_dict = torch.load(args.pre_trained, map_location='cpu')
    model.load_state_dict(state_dict)
    model.eval()
    return model

def haircut():
    import argparse
    import matplotlib.pyplot as plt
    #接收傳送圖片
    parser = argparse.ArgumentParser(description='Semantic Segmentation')

    # Arguments
    parser.add_argument('--data-folder', type=str, default='./data/hair',help='name of the data folder (default: ./data/hair)')
    parser.add_argument('--batch-size', type=int, default=1,help='batch size (default: 8)')
    parser.add_argument('--pre-trained', type=str, default='./checkpoints/model.pt',help='path of pre-trained weights (default: None)')

    args = parser.parse_args()
    args.device = torch.device("cpu")

    image_files = sorted(glob('{}/*.jp*g'.format(args.data_folder)))
    model = load_model(args)
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
    ])

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

if __name__=='__main__':
    haircut()
