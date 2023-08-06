import torch
from torch.optim import AdamW
import torch.nn as nn
from torch.utils.data import DataLoader
from matplotlib import pyplot as plt
import tqdm

import numpy as np
import pandas as pd

from dataset import SpiderDataset


def test_duplicates(dataset_1, dataset_2):
    df = pd.concat([dataset_1.df, dataset_2.df])
    assert len(df) - len(df.drop_duplicates()) == 0, f"Datasets {dataset_1} and {dataset_2} contain duplicates"


if __name__ == "__main__":
    # hyperparameters and variables
    N_EPOCH = 200
    BATCH_SIZE = 64
    LEARNING_RATE = 0.0001
    INPUT_FILE_PATH = "leg_movement_data.csv"
    OUTPUT_MODEL_PATH = "model_v0.pth"
    
    # get datasets and dataloaders
    train_dataset = SpiderDataset(INPUT_FILE_PATH, split="train")
    val_dataset = SpiderDataset(INPUT_FILE_PATH, split="val")
    test_dataset = SpiderDataset(INPUT_FILE_PATH, split="test")
    
    test_duplicates(train_dataset, val_dataset)
    test_duplicates(train_dataset, test_dataset)
    test_duplicates(val_dataset, test_dataset)

    train_dataloader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    val_dataloader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False)
    test_dataloader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)
    
    # define the model
    sample = train_dataset[0]
    input_size = len(sample[0])
    output_size = len(sample[1])

    model = nn.Sequential(nn.Linear(input_size, 128, dtype=torch.float64), 
                        nn.ReLU(), 
                        nn.Linear(128, 64, dtype=torch.float64), 
                        nn.ReLU(), 
                        nn.Linear(64, 64, dtype=torch.float64), 
                        nn.ReLU(), 
                        nn.Linear(64, 32, dtype=torch.float64), 
                        nn.ReLU(), 
                        nn.Linear(32, output_size, dtype=torch.float64))

    # define loss & optimizer
    loss_fn = nn.MSELoss()
    optimizer = AdamW(model.parameters(), lr=LEARNING_RATE)
    
    # train loop
    t = tqdm.tqdm(range(N_EPOCH))
    for epoch in t:
        
        train_loss = []
        
        for batch_x, batch_y in train_dataloader:
            # get predictions for each batch
            pred_y = model(batch_x)
            # compute loss
            loss = loss_fn(batch_y, pred_y)
            
            # backpropagate and do an optim. step
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            with torch.no_grad():        
                train_loss.append(loss.cpu().detach().item())
            
        model.eval()
        with torch.no_grad():
            # occasionally, compute the validation loss.
            val_loss = []
            for batch_x, batch_y in val_dataloader:
                pred_y = model(batch_x)
                loss = torch.mean((batch_y - pred_y) ** 2, dim=0)
                
                val_loss.append(loss.cpu().detach().numpy())
                
        val_loss = np.round(np.mean(val_loss, axis=0), 6)
        t.set_description("TRAIN loss: %f - VAL loss: [%f, %f, %f]" % (np.round(np.mean(train_loss), 6), *val_loss))
        
    # save the trained model
    torch.save(model, OUTPUT_MODEL_PATH)
