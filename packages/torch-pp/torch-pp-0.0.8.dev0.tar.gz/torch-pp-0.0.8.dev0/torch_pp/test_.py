import numpy as np
import torch

from torch_pp import StandardScaler


def test_scalers():
    x = torch.from_numpy(np.array([[20], [-3], [-11]]))
    x_ = StandardScaler().fit_transform(x)
    pass
