import torch
import numpy as np
from torch.utils.data import DataLoader

from dataset import SpiderDataset

if __name__ == "__main__":
    
    INPUT_FILE_PATH = "leg_movement_data.csv"
    INPUT_MODEL_PATH = "model_v0.pth"
    BATCH_SIZE = 1024

    # get the test dataset
    test_dataset = SpiderDataset(INPUT_FILE_PATH, split="test")
    test_dataloader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)
    
    print(test_dataset.df.columns)
    
    # load the model
    model = torch.load("model_v0.pth")
    model.eval()

    with torch.no_grad():
        # compute the test loss.
        test_loss = []
        for batch_x, batch_y in test_dataloader:
            pred_y = model(batch_x)
            loss = (batch_y - pred_y) ** 2
            
            test_loss.append(loss.cpu().detach().numpy())
            
    test_loss = np.concatenate(test_loss, axis=0)
    test_loss = np.mean(test_loss, axis=0)
    print("TEST LOSS: ", test_loss)
