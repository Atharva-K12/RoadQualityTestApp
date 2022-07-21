import torch.cuda as cuda
import torch
device=torch.device("cuda:0" if cuda.is_available() else "cpu")
import torch.nn as nn
import torch.nn.functional as F