import torch
import torch.multiprocessing
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.data as data_utils
from torch.utils.data import Dataset, DataLoader
import numpy as np
import time
import os
from datetime import datetime

from packet_parser import *
from feature_construction import *
from gen_net_model_cnn import *

def model_main():
    tick = datetime.now()

    capture_dir = "captures/"
    cleaned_datasets_dir = "parsed_captures/"
    numpy_dir = "numpy_files/"
    conv_dir = "datasets_conv/"

    # --- UPDATED: The number of features is now 128 ---
    features = 128 
    # --- UPDATED: These dimensions are needed for the 4D array ---
    packet_height = 8
    packet_width = 16

    # Change these for tuning
    iterations = 601
    alpha = 1e-5
    hidden_nodes = 32
    classes = 4
    batch_size = 128
    num_data_files = 1

    x_files, y_files, dataset_files, cleaned_files = [], [], [], []

    print("\nCreating necessary file lists.\n")

    # builds necessary file list
    for i in range(0, num_data_files):
        filename = os.path.join("w_dataset"+str(i)+".txt")
        dataset_files.append(filename)

        cleaned_file = os.path.join(cleaned_datasets_dir,"w_dataset"+str(i)+"_parsed.txt")
        cleaned_files.append(cleaned_file)

        x_file= os.path.join(numpy_dir, "w_dataset"+str(i)+"_features.npy")
        x_files.append(x_file)
        
        y_file= os.path.join(numpy_dir, "w_dataset"+str(i)+"_labels.npy")
        y_files.append(y_file)

    print("Completing Preprocessing...")
    print("Dataset Files: ", len(dataset_files),"\nCleaned Files: ", len(cleaned_files), "\nx_files: ", len(x_files), "\ny_files: ", y_files)
    
    # --- UPDATED: The call to preprocessor_main now includes new arguments ---
    preprocessor_main(features, dataset_files, cleaned_files, x_files, y_files, packet_height, packet_width)
    
    # --- NEW: Load the training data before calling the model function ---
    x_train_numpy = np.load(x_files[0])
    y_labels_numpy = np.load(y_files[0])
    
    x_train = torch.from_numpy(x_train_numpy).float()
    y_labels = torch.from_numpy(y_labels_numpy).long().flatten()

    print("\nTraining CNN Model...\n")
    
    # --- UPDATED: The call to gen_net_cnn_main now includes all 10 arguments ---
    gen_net_cnn_main(x_train, y_labels, x_files, y_files, features, iterations, hidden_nodes, classes, alpha, batch_size)

if __name__ == "__main__":
    model_main()
