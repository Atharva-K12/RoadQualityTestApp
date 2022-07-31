import os
from PIL import Image
from torch.utils.data import Dataset
import numpy as np
import matplotlib.pyplot as plt
import torch
import torchvision
img_size=64
transform = torchvision.transforms.Compose([
    torchvision.transforms.Resize((img_size, img_size)),
    torchvision.transforms.RandomHorizontalFlip(),
    torchvision.transforms.ToTensor(),])
class RTKDataset(Dataset):
    def __init__(self, image_dir, mask_dir,imagesize=128,inchannels=3,outchannels=1):
        self.transform =torchvision.transforms.Compose([
            torchvision.transforms.Resize((imagesize, imagesize)),
            torchvision.transforms.ToTensor(),])
        self.image_dir = image_dir
        self.mask_dir = mask_dir
        self.images = os.listdir(image_dir)

    def __len__(self):
        return len(self.images)

    def __getitem__(self, index):
        img_path = os.path.join(self.image_dir, self.images[index])
        mask_path = os.path.join(self.mask_dir, self.images[index])#.replace(".png", "GT.png"))
        image=self.transform(Image.open(img_path))
        mask=self.transform(Image.open(mask_path))
        # image = np.array(Image.open(img_path).convert("RGB"))
        # mask = np.array(Image.open(mask_path).convert("L"), dtype=np.float32)
        mask[mask == 255.0] = 1.0
        return image, mask


if __name__ == "__main__":
    image_dir = "../../../RTK_SemanticSegmentationGT_originalFrames"
    mask_dir = "../../../RTK_SemanticSegmentationGT_NoColorMapMasks/RTK_SemanticSegmentationGT_NoColorMapMasks"
    dataset = RTKDataset(image_dir, mask_dir)
    plt.imshow(dataset[0][0].permute(1, 2, 0))
    plt.show()
    plt.imshow(dataset[0][1].permute(1,2,0), cmap="gray")
    plt.show()
    # print(dataset[0][1])
