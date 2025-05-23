import torch
import torch.multiprocessing
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.data as data_utils
from torch.utils.data import Dataset, DataLoader
import numpy as np
import time
import os

from packet_parser import *
from feature_construction import *
#from statistics import *

from gen_net_model_mlp import *

'''
This function loads the training files and labels
It then determines the number of features to create x and y matrices
'''
def file_loader(x_train_file, y_train_file, classes):
    numpy_x_train = np.load(x_train_file)
    numpy_x_train = np.transpose(numpy_x_train) #transpose = reverses dimensions of an array. Goes fom (x,y) to (y,x)
    x_train = torch.from_numpy(numpy_x_train).float()
    
    numpy_y_train = np.load(y_train_file)
    #numpy_y_train = transpose(numpy_y_train)
    y_train = torch.from_numpy(numpy_y_train)
    y_labels = torch.zeros(x_train.shape[0], classes)

    feature_count = x_train[1]

    for i in range(y_train.shape[1]):
        y_val = int(y_train[0][i])
        y_labels[i][y_val] = 1 #SAY WHY
    return x_train, y_labels, feature_count

def model_main():
    tick = datetime.now()

    capture_dir = "captures/"
    cleaned_datasets_dir = "parsed_captures/"
    numpy_dir = "numpy_files/"
    conv_dir = "datasets_conv/" #this directory is for...

    #change these for tuning
    features = 84 #packet_parser.py multiplies by 2 to get bytes
    iterations = 601
    alpha = 1e-5
    hidden_nodes = 32
    classes = 4
    batch_size = 128
    num_data_files = 4

    x_files, y_files, dataset_files, cleaned_files = [], [], [], []

    x_train_file = numpy_dir +"w_dataset0_features.npy"
    y_train_file = numpy_dir + "w_dataset0_labels.npy"

    print("\nCreating necessary file lists.\n")

    #builds necessary file list
    for i in range(0, num_data_files):
        #standardize capture, parsed, and csv names
        filename = os.path.join("w_dataset"+str(i)+".txt")
        dataset_files.append(filename)

        cleaned_file = os.path.join(cleaned_datasets_dir,"w_dataset"+str(i)+"_parsed.txt")
        cleaned_files.append(cleaned_file)

        x_file= os.path.join(numpy_dir, "w_dataset"+str(i)+"_features.npy")
        x_files.append(x_file)
        
        y_file= os.path.join(numpy_dir, "w_dataset"+str(i)+"_labels.npy")
        y_files.append(y_file)

    #preproccess_main() in feature_construction.py
    print("Completing Preprocessing...")
    print("Dataset Files: ", len(dataset_files),"\nCleaned Files: ", len(cleaned_files), "\nx_files: ", len(x_files), "\ny_files: ", y_files)
    preprocessor_main(features, dataset_files, cleaned_files, x_files, y_files)
    
    for i in range(0,1):
        print("\nTraining File Loader With:\n")
        print(x_train_file)
        print(y_train_file)

        x_train, y_labels, feature_count = file_loader(x_train_file, y_train_file, classes)

        print("\nCalling MLP Model...\n")

        #from gen_net_mlp.py
        gen_net_mlp_main(x_train, y_labels, x_files, y_files, feature_count, iterations, hidden_nodes, classes, alpha, batch_size)

if __name__ == "__main__":
    main()
