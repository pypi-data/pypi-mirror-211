import numpy as np
from offset_predictor import OffsetPredictor

if __name__ == "__main__":
    off_pred = OffsetPredictor(model_path="model_v0.pth")

    sample_data = np.concatenate([np.random.randn(21), np.zeros(5)])
    random_one = np.random.randint(1, 6)
    sample_data[-random_one] = 1
    print(sample_data)

    offset = off_pred(sample_data)
    print(offset)
