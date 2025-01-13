import torch
import torchvision.transforms as transforms
from PIL import Image
import torch.nn as nn
import numpy as np
import cv2
print('--------------s-ready----------------')
class CNN_Segmentation_Model(nn.Module):
    def __init__(self, input_channels=3):
        super(CNN_Segmentation_Model, self).__init__()

        # 编码器部分
        self.encoder = nn.Sequential(
            nn.Conv2d(input_channels, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),

            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),

            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),

            nn.Conv2d(256, 512, kernel_size=3, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )
        self.middle = nn.Conv2d(512, 512, kernel_size=3, padding=1)
        # 解码器部分
        self.decoder = nn.Sequential(
            nn.Conv2d(512, 512, kernel_size=3, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU(),
            nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True),

            nn.Conv2d(512, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True),

            nn.Conv2d(256, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True),

            nn.Conv2d(128, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True),
        )

        # 输出层
        self.output_layer = nn.Conv2d(64, 1, kernel_size=1)

    def forward(self, x):
        # 编码器部分
        x = self.encoder(x)
        x = self.middle(x)
        x = self.middle(x)
        # 解码器部分
        x = self.decoder(x)
        # 输出层
        x = self.output_layer(x)
        return x

model = CNN_Segmentation_Model()
model.load_state_dict(torch.load("sega.pth", map_location=torch.device('cpu')))

def first_clean(image):# input 0-1 image | output black-cleaned 0-1 image
    contours, _ = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    max_contour = max(contours, key=cv2.contourArea)
    white_image = np.ones_like(image) * 0
    cv2.drawContours(white_image, [max_contour], -1, 255, thickness=cv2.FILLED)
    return white_image

def pad_to_square(image, output_path):#input RGB image and output path| save squared image and output square image
    width, height = image.size
    # 计算新的尺寸（取较大的边作为新的尺寸）
    new_size = max(width, height)

    # 创建一个黑色的背景图像，尺寸为 new_size x new_size
    new_image = Image.new('RGB', (new_size, new_size), (0, 0, 0))  # '0, 0, 0' 表示黑色
    left = (new_size - width) // 2
    top = (new_size - height) // 2
    new_image.paste(image, (left, top))
    new_image.save(output_path)
    return new_image

def segmentmodel(model,path):#input path of image | output square image
    transform_x = transforms.Compose([
        transforms.Resize((256, 256)),  # 调整大小
        transforms.ToTensor(),         # 转换为张量
    ])

    imge=Image.open(path).convert('RGB')
    width,height=imge.size

    img=transform_x(imge)
    img=img.unsqueeze(0)

    out=model(img)

    o=out.squeeze().detach().numpy()
    o = (o >= 0.500).astype(int)
    o=np.array(o,dtype=np.uint8)*255

    mask=first_clean(o)
    mask=cv2.resize(mask,(width,height))

    rgb_array = np.array(imge)
    binary_array = np.array(mask)

    black_background = np.zeros_like(rgb_array)
    mask = binary_array == 255
    # 在黑色背景上抠出 RGB 图片对应的白色部分
    black_background[mask] = rgb_array[mask]
    output_image = Image.fromarray(black_background)
    # new=pad_to_square(output_image,savepath)
    return output_image

