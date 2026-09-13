import torch
from torchvision import transforms
import random
from PIL import Image

def get_hair_classification_transforms(train: bool = True):
    """Data augmentation pipelines for hair classification."""
    normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                     std=[0.229, 0.224, 0.225])
    
    if train:
        return transforms.Compose([
            transforms.RandomResizedCrop(224),
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(15),
            transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
            transforms.ToTensor(),
            normalize
        ])
    else:
        return transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            normalize
        ])

class SynchronizedTransform:
    """Synchronized data augmentation for image + mask pairs."""
    def __init__(self, img_size=(256, 256)):
        self.img_size = img_size
        
    def __call__(self, image: Image.Image, mask: Image.Image):
        # Resize
        image = image.resize(self.img_size, Image.BILINEAR)
        mask = mask.resize(self.img_size, Image.NEAREST)
        
        # Random horizontal flip
        if random.random() > 0.5:
            image = image.transpose(Image.FLIP_LEFT_RIGHT)
            mask = mask.transpose(Image.FLIP_LEFT_RIGHT)
            
        # To Tensor
        img_tensor = transforms.ToTensor()(image)
        mask_tensor = transforms.ToTensor()(mask)
        
        # Normalize image
        img_tensor = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                          std=[0.229, 0.224, 0.225])(img_tensor)
                                          
        return img_tensor, mask_tensor
