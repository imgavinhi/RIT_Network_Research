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
    numpy_x_train = np.transpose(numpy_x_train) #transpose = DEFINE
    x_train = torch.from_numpy(numpy_x_train).float()
    
    numpy_y_train = np.load(y_train_file)
    #numpy_y_train = transpose(numpy_y_train)
    y_train = torch.from_numpy(numpy_y_train)
    y_labels = torch.zeros(x_train.shape[0], classes) #DEFINE

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

    features = 84
    iterations = 1000
    alpha = 1e-6
    hidden_nodes = 60
    classes = 4
    batch_size = 4000 
    num_data_files = 4

    x_files, y_files, dataset_files, cleaned_files = [], [], [], []

    x_train_file = numpy_dir +"w_dataset0_features.npy"
    y_train_file = numpy_dir + "w_dataset0_labels.npy"

    print("\nCreating necessary file lists.\n")

    #builds necessary file list
    for i in range(0, num_data_files):
        #standardize capture, parsed, and csv names
        #filename = os.path.join(capture_dir, "w_dataset"+str(i)+".txt")
        filename = os.path.join("w_dataset"+str(i)+".txt")
        dataset_files.append(filename)

        cleaned_file = os.path.join(cleaned_datasets_dir,"w_dataset"+str(i)+"_parsed.txt")
        cleaned_files.append(cleaned_file)

        x_file= os.path.join(numpy_dir, "w_dataset"+str(i)+"_features.npy")
        x_files.append(x_file)
        
        y_file= os.path.join(numpy_dir, "w_dataset"+str(i)+"_labels.npy")
        y_files.append(y_file)

    #preproccess_main() in feature construction
    print("Completing Preprocessing...")
    preprocessor_main(features, dataset_files, cleaned_files, x_files, y_files)
    
    for i in range(0,1):
        print("\nTraining File Loader With:\n")
        print(x_train_file)
        print(y_train_file)

        x_train, y_labels, feature_count = file_loader(x_train_file, y_train_file, classes)

        print("\nCalling MLP Model...\n")

        gen_net_mlp_main(x_train, y_labels, x_files, y_files, feature_count, iterations, hidden_nodes, classes, alpha, batch_size)

if __name__ == "__main__":
    main()
