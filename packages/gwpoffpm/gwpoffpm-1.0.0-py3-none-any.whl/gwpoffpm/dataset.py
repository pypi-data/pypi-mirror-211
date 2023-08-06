import torch
from torch.utils.data import Dataset
import pandas as pd
import numpy as np


def lookup(df, row_labels, col_labels, column_name=None):
    up = pd.DataFrame(df.to_numpy()[df.index.get_indexer(row_labels), df.columns.get_indexer(col_labels)])
    if column_name is not None:
        up.columns = [column_name]
    return up


class SpiderDataset(Dataset):
    
    y_stats = None
    
    def __init__(self, filepath, split, split_perc=[0.0, 0.7, 0.85, 1.0], seed=10):
        # load the data from file
        self.df = pd.read_csv(filepath)
        # is this drop ok?
        self.df = self.df.drop(self.df[self.df["number_of_tries"] > 10].index)
        self.df = self.df.dropna()
        self.df.index = np.arange(len(self.df))
        
        assert split in {"full", "train", "val", "test"}
        
        # split the data. in a single experiment all datasets should be inizialized with the same seed to prevent data leaking.
        np.random.seed(seed)
        indices = np.random.permutation(np.arange(len(self.df)))
        if split == "train":
            self.df = self.df.iloc[indices[int(split_perc[0] * len(self.df)):int(split_perc[1] * len(self.df))]]
        elif split == "val":
            self.df = self.df.iloc[indices[int(split_perc[1] * len(self.df)):int(split_perc[2] * len(self.df))]]
        elif split == "test":
            self.df = self.df.iloc[indices[int(split_perc[2] * len(self.df)):int(split_perc[3] * len(self.df))]]
            
        # onehot encode the "leg to move" attribute
        onehot_legs = pd.get_dummies(self.df["leg_to_move_id"]).astype(float)
        onehot_legs.columns = ["leg_to_move_" + str(i) for i in range(5)]
        self.df = self.df.join(onehot_legs)
        
        # extract actual x,y,z positions after 
        after_x_columns = "xA_after_" + self.df["leg_to_move_id"].astype(int).astype(str) + "_x"
        after_x = lookup(self.df, after_x_columns.index, after_x_columns)[0]
        after_x.index = self.df["xC_x"].index
        
        after_y_columns = "xA_after_" + self.df["leg_to_move_id"].astype(int).astype(str) + "_y"
        after_y = lookup(self.df, after_y_columns.index, after_y_columns)[0]
        after_y.index = self.df["xC_y"].index
        
        after_z_columns = "xA_after_" + self.df["leg_to_move_id"].astype(int).astype(str) + "_z"
        after_z = lookup(self.df, after_z_columns.index, after_z_columns)[0]
        after_z.index = self.df["xC_z"].index
        
        # get the xyz offsets
        self.y = pd.concat((after_x - self.df["xC_x"],
                            after_y - self.df["xC_y"],
                            after_z - self.df["xC_z"]), axis="columns")
        self.y.columns = ["x_offset", "y_offset", "z_offset"]
        
        if split in {"train", "full"}:
            SpiderDataset.y_stats = {"mu": torch.tensor(np.mean(self.y.to_numpy(), axis=0), dtype=torch.float64),
                                     "sigma": torch.tensor(np.std(self.y.to_numpy(), axis=0), dtype=torch.float64)}
        
        # delete unneeded columns.
        to_delete = [column for column in self.df.columns if "after" in column] + ["leg_to_move_id", "number_of_tries"] + [column for column in self.df.columns if "bno" in column]
        self.df = self.df.drop(columns=to_delete)
        
        
    def __len__(self):
        return len(self.df)
    
    def __getitem__(self, index):
        x = self.df.iloc[index]
        y = self.y.iloc[index]
        
        y = torch.tensor(y, dtype=torch.float64)
        
        # one could optionally normalize by the mean and std to increase stability of nn. non needed for now.
        # y = (y - SpiderDataset.y_stats["mu"]) / SpiderDataset.y_stats["sigma"]
        
        return torch.tensor(x, dtype=torch.float64), y