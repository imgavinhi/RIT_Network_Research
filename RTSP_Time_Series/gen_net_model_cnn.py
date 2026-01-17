import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.data as data_utils
from datetime import datetime
import os.path
from predictions import *

# Defines the main operations for the machine learning neural network
def gen_net_cnn_main(x_train, y_labels, x_file_list, y_file_list, feature_count, iterations, hidden_nodes, classes, alpha, batch_size):
    # UPDATED: Dimensions for the 12-packet RTSP Time Series
    packet_height = 12
    packet_width = 148
    d_out = classes
    
    # NEW MATH: (64 channels * 3 height * 37 width) = 7104
    # This matches the result after two 2x2 MaxPool layers on a 12x148 input
    flatten_size = 64 * 3 * 37
    
    print("Model Params:", feature_count, iterations, hidden_nodes, classes, alpha, batch_size)

    epochs = iterations
    train = data_utils.TensorDataset(x_train, y_labels)
    train_loader = data_utils.DataLoader(train, batch_size=batch_size, shuffle=False, num_workers=0)

    # CNN Architecture optimized for Time Series "Images"
    net_model = torch.nn.Sequential(
        # Layer 1: Conv -> ReLU -> MaxPool
        # Input: (Batch, 1, 12, 148)
        nn.Conv2d(in_channels=1, out_channels=32, kernel_size=3, padding=1),
        nn.ReLU(),
        nn.MaxPool2d(kernel_size=2), # Result: (32, 6, 74)

        # Layer 2: Conv -> ReLU -> MaxPool
        nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, padding=1),
        nn.ReLU(),
        nn.MaxPool2d(kernel_size=2), # Result: (64, 3, 37)

        # Flatten for Linear Layers
        nn.Flatten(),

        # Fully Connected Layers
        nn.Linear(flatten_size, hidden_nodes), 
        nn.ReLU(),
        
        nn.Linear(hidden_nodes, d_out)
    )

    use_cuda = torch.cuda.is_available()
    device = torch.device("cuda:0" if use_cuda else "cpu")
    net_model.to(device)
    
    print("Device:", device)
    print("X Shape:", x_train.size())
    print("Y Shape:", y_labels.size())

    loss_function = torch.nn.CrossEntropyLoss()
    optimizer = optimizer_pick(1, net_model, alpha)

    tick = datetime.now()

    # Training Loop
    for epoch in range(epochs):
        for i, data in enumerate(train_loader, 1):
            inputs, targets = data
            inputs, targets = inputs.to(device), targets.to(device)

            y_pred = net_model(inputs.float())
            loss = loss_function(y_pred, targets)
            
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        if (epoch + 1) % 10 == 0 or epoch == 0:
            print(f"Epoch {epoch + 1}/{epochs} completed. Loss: {loss.item():.10f}")

        # Early stopping if loss is sufficiently low
        if loss.item() < 1e-10:
            print(f"Target loss reached at epoch {epoch}")
            break

    torch.save(net_model.state_dict(), 'params.pt')
    tock = datetime.now()
    print("\nDone with training. Total time: ", tock - tick)

    # Dataset Testing and Reporting
    print("\nStarting dataset testing...")
    net_model.eval() # Set to evaluation mode

    for i in range(len(x_file_list)):
        x_test_path = x_file_list[i]
        y_test_path = y_file_list[i]
        
        # --- HOST IDENTIFICATION LOGIC ---
        # Load host IP mapping created during feature construction
        hosts_file = x_test_path.replace("features.npy", "hosts.npy")
        host_data = None
        if os.path.exists(hosts_file):
            host_data = np.load(hosts_file)

        x_test_loaded = np.load(x_test_path)
        x_test_tensor = torch.from_numpy(x_test_loaded).float().to(device)

        y_test_loaded = np.load(y_test_path)
        y_test_labels = torch.from_numpy(y_test_loaded).long().flatten().to(device)
        
        with torch.no_grad():
            y_test_pred = net_model(x_test_tensor)
            predicted_classes = torch.argmax(y_test_pred, dim=1)

        # Pass results and IP data to predictions.py for the report
        predicted_numpy = predicted_classes.cpu().numpy()
        packet_choice(predicted_numpy, host_data=host_data)
        
        accuracy(predicted_classes, y_test_labels)

def accuracy(predictions, y_test):
    correct_predictions = (predictions == y_test).sum().item()
    total = y_test.size(0)
    print(f"Total Predictions: {total} Accuracy Count: {correct_predictions}")
    print(f"Accuracy of Predictions: {correct_predictions / total if total > 0 else 0:.4f}\n")

def optimizer_pick(choice, net_model, alpha):
    return torch.optim.Adam(net_model.parameters(), lr=alpha)