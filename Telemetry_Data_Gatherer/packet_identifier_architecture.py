import torch
import torch.multiprocessing
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.data as data_utils
from torch.utils.data import Dataset, DataLoader
import numpy as np
import time

from packet_parser import *
from feature_construction import *
#from statistics import *

'''
This function loads the training files and labels
It then determines the number of features to create x and y matrices
'''
def file_loader(x_train_file, y_train_file, classes):
    numpy_x_train = np.load(x_train_file)
    numpy_x_train = np.transpose(numpy_x_train) #transpose = DEFINE
    x_train = torch.from_numpy(numpy_x_train).float()
    
    numpy_y_train = np.load(y_train_file)
    numpy_y_train = transpose(numpy_y_train)
    y_train = torch.from_numpy(numpy_y_train)
    y_labels = torch.zeros(x_train.shape[0], classes) #DEFINE

    feature_count = x_train_shape[1]

    for i in range(y_train.shape[1]):
        y_val = int(y_train[0][j])
        y_labels[j][y_val] = 1 #SAY WHY
    return x_train, y_labels, feature_count

def main():
    pas

if __name__ == "__main__":
    main()
