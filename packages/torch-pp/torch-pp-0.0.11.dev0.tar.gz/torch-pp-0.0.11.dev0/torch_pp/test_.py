import numpy as np
import torch

from torch_pp import StandardScaler

if __name__ == '__main__':
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    x = torch.from_numpy(np.array([[20, 1], [-3, 700], [-11, 3]])).to(device)
    x_ = StandardScaler().fit_transform(x)
    pass
