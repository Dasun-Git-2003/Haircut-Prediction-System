import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from datasets import load_dataset
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DiceLoss(nn.Module):
    def __init__(self, smooth=1.0):
        super(DiceLoss, self).__init__()
        self.smooth = smooth

    def forward(self, inputs, targets):
        inputs = torch.sigmoid(inputs)
        inputs = inputs.view(-1)
        targets = targets.view(-1)
        intersection = (inputs * targets).sum()
        dice = (2.*intersection + self.smooth)/(inputs.sum() + targets.sum() + self.smooth)
        return 1 - dice

class SegmentationDataset(Dataset):
    def __init__(self, hf_dataset, img_size=(256, 256)):
        self.dataset = hf_dataset
        self.img_size = img_size
        self.img_transform = transforms.Compose([
            transforms.Resize(img_size),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        self.mask_transform = transforms.Compose([
            transforms.Resize(img_size),
            transforms.ToTensor()
        ])

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        item = self.dataset[idx]
        image = item['image'].convert('RGB')
        # Mask is expected to be L mode, values 0 or 255
        mask = item['mask'].convert('L')
        
        image = self.img_transform(image)
        mask = self.mask_transform(mask)
        # Convert mask to 0/1
        mask = (mask > 0.5).float()
        
        return image, mask

def train_segmentation():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    logger.info(f"Training on device: {device}")
    
    ds = load_dataset("nobg/figaro1k")
    train_ds = SegmentationDataset(ds['train'])
    test_ds = SegmentationDataset(ds['test'])
    
    train_loader = DataLoader(train_ds, batch_size=16, shuffle=True)
    test_loader = DataLoader(test_ds, batch_size=16, shuffle=False)
    
    from torchvision.models.segmentation import deeplabv3_mobilenet_v3_large
    model = deeplabv3_mobilenet_v3_large(pretrained=False, num_classes=1)
    model = model.to(device)
    
    bce_loss = nn.BCEWithLogitsLoss()
    dice_loss = DiceLoss()
    
    optimizer = optim.Adam(model.parameters(), lr=1e-4)
    epochs = 30
    
    os.makedirs('../saved_models', exist_ok=True)
    best_loss = float('inf')
    
    for epoch in range(epochs):
        model.train()
        train_loss = 0.0
        for imgs, masks in train_loader:
            imgs, masks = imgs.to(device), masks.to(device)
            
            optimizer.zero_grad()
            outputs = model(imgs)['out']
            
            loss = bce_loss(outputs, masks) + dice_loss(outputs, masks)
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item()
            
        model.eval()
        val_loss = 0.0
        with torch.no_grad():
             for imgs, masks in test_loader:
                 imgs, masks = imgs.to(device), masks.to(device)
                 outputs = model(imgs)['out']
                 v_loss = bce_loss(outputs, masks) + dice_loss(outputs, masks)
                 val_loss += v_loss.item()
                 
        avg_val_loss = val_loss / len(test_loader)
        logger.info(f"Epoch {epoch+1}/{epochs} | Val Loss: {avg_val_loss:.4f}")
        
        if avg_val_loss < best_loss:
            best_loss = avg_val_loss
            torch.save(model.state_dict(), '../saved_models/hair_segmentation_model.pth')
            logger.info("Saved best segmentation model")

if __name__ == "__main__":
    train_segmentation()
