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
    numpy_y_train = transpose(numpy_y_train)
    y_train = torch.from_numpy(numpy_y_train)
    y_labels = torch.zeros(x_train.shape[0], classes) #DEFINE

    feature_count = x_train_shape[1]

    for i in range(y_train.shape[1]):
        y_val = int(y_train[0][j])
        y_labels[j][y_val] = 1 #SAY WHY
    return x_train, y_labels, feature_count

def main():
    tick = datetime.now()

    script_dir = 

    capture_dir = "\\capture"
    cleaned_datasets_dir = "\\parsed_captures"
    numpy_dir = "\\numpy_files"
    conv_dir = "\\dataset_conv" #this directory is for...

    features = 11
    iterations = 101
    alpha = 1e-5
    hidden_nodes = 28
    classes = 14
    bacth_size = 128 
    num_data_files = 3

    x_files, y_files, dataset_files, cleaned_files = [], [], [], []

    x_train_file = numpy_dir + +"w_dataset0_features.npy"
    y_train_file = numpy_dir + "w_dataset0_labels.npy"

    print("\nCreating necessary file lists.\n")

    #builds necessary file list
    for i in range_(0, num_data_files):
        #standardize capture, parsed, and csv names
        filename = capture_dir+"dataset"+str(i)+".txt"
        dataset_fies.append(filename)

        cleaned_file = cleaned_dataset_dir+"w_dataset"+str(i)+".txt"
        cleaned_files.append(cleaned_file)

        X_file=numpy_dir+"w_dataset"+str(i)+"_features.npy"
        X_test_files.append(X_file)
        
        Y_file=numpy_dir+"w_dataset"+str(i)+"_labels.npy"
        Y_test_files.append(Y_file)

    #preproccess_main() in feature construction
    print("Completing Preprocessing...")
    preprocessor_main(features, dataset_files, cleaned_files, x_files, y_files)
    
    for i in range(0,1):
        print("\nTraining File Loader With:\n")
        print(x_train_file)
        print(y_train_file)

        x_train, y_labels, feature_count = file_loader(x_train_file, y_train_file, classes)

        print("\nCalling MLP Model...\n")

        gen_net_mlp_model(x_train, y_labels, x_files, y_files, feature_count, iterations, hidden_nodes, classes, alpha, batch_size)

if __name__ == "__main__":
    main()