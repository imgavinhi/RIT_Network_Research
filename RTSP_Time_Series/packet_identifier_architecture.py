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

# Custom modules for the packet-to-matrix pipeline
from packet_parser import *
from feature_construction import *
from gen_net_model_cnn import *

def model_main():
    tick = datetime.now()

    # Directory configuration
    capture_dir = "captures/"
    cleaned_datasets_dir = "parsed_captures/"
    numpy_dir = "numpy_files/"
    conv_dir = "datasets_conv/"

    # --- RTSP Time Series Dimensions ---
    # We use 26 packets (time) and 148 bytes (features) per slide findings 
    # Doubling the conversation size from 13 to 26 improved results [cite: 27, 28]
    packet_height = 12 
    packet_width = 148 
    features = packet_height * packet_width

    # --- Machine Learning Hyperparameters ---
    iterations = 100
    alpha = 1e-4
    hidden_nodes = 32
    
    # Classes: 0:Background, 1:RTSP Success (2xx), 2:RTSP Client Error (4xx), 3:RTSP Server Error (5xx)
    classes = 4 
    batch_size = 64
    num_data_files = 2

    x_files, y_files, dataset_files, cleaned_files = [], [], [], []

    print("\nCreating necessary file lists.\n")

    # Builds necessary file lists for the training pipeline
    for i in range(0, num_data_files):
        # Raw packet text files
        filename = os.path.join("w_dataset"+str(i)+".txt")
        dataset_files.append(filename)

        # Cleaned hex data files
        cleaned_file = os.path.join(cleaned_datasets_dir,"w_dataset"+str(i)+"_parsed.txt")
        cleaned_files.append(cleaned_file)

        # Feature matrices (2D representation of the packet flows) [cite: 22]
        x_file= os.path.join(numpy_dir, "w_dataset"+str(i)+"_features.npy")
        x_files.append(x_file)
        
        # Sequence labels (one label per conversation) [cite: 11]
        y_file= os.path.join(numpy_dir, "w_dataset"+str(i)+"_labels.npy")
        y_files.append(y_file)

    print("Completing Preprocessing...")
    print("Dataset Files: ", len(dataset_files),"\nCleaned Files: ", len(cleaned_files), "\nx_files: ", len(x_files), "\ny_files: ", y_files)
    
    # Preprocessor organizes the data into the matrix structure required by the CNN [cite: 22, 32]
    preprocessor_main(features, dataset_files, cleaned_files, x_files, y_files, packet_height, packet_width)
    
    # Load the newly constructed training data for the neural network
    x_train_numpy = np.load(x_files[0])
    y_labels_numpy = np.load(y_files[0])
    
    # Convert NumPy arrays to Torch tensors
    x_train = torch.from_numpy(x_train_numpy).float()
    y_labels = torch.from_numpy(y_labels_numpy).long().flatten()

    print("\nTraining CNN Model for RTSP Status Code Recognition...\n") # 
    
    # Execute the CNN training and testing loop
    gen_net_cnn_main(x_train, y_labels, x_files, y_files, features, iterations, hidden_nodes, classes, alpha, batch_size)

    tock = datetime.now()
    print(f"\nTotal Execution Time: {tock - tick}")

if __name__ == "__main__":
    model_main()