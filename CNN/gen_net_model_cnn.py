import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.data as data_utils

from datetime import datetime
import os.path
from predictions import *

# defines the main operations for the machine learning neural network
def gen_net_cnn_main(x_train, y_labels, x_file_list, y_file_list, feature_count, iterations, hidden_nodes, classes, alpha, batch_size):
    # Set up the new packet dimensions for the CNN
    packet_height = 8
    packet_width = 16
    d_in = feature_count  # This is the original 128
    
    # Calculate the new flattened input size for the fully connected layers
    # After two MaxPool2d layers (kernel_size=2), height is 8/2/2 = 2, and width is 16/2/2 = 4
    h2 = hidden_nodes
    h1 = hidden_nodes * 2
    d_out = classes
    
    # Model parameters
    print("Model Basic Params:", feature_count, iterations, hidden_nodes, classes, alpha, batch_size)

    iteration_ctr = 0
    epochs = iterations

    max_tier = 20
    train = data_utils.TensorDataset(x_train, y_labels)
    train_loader = data_utils.DataLoader(train, batch_size=batch_size, shuffle=False, num_workers=0)

    # --- Replaced MLP with CNN Architecture ---
    net_model = torch.nn.Sequential(
        # First convolutional layer: expects a 4D input of (batch, 1, 14, 14)

        #make the problem hard for CNN!

        nn.Conv2d(in_channels=1, out_channels=32, kernel_size=3, padding=1),
        nn.ReLU(),
        nn.MaxPool2d(kernel_size=2),

        # Second convolutional layer
        nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, padding=1),
        nn.ReLU(),
        nn.MaxPool2d(kernel_size=2),

        # Flatten the output for the fully connected layers
        nn.Flatten(),

        # Linear layer with the new flattened input size (64 channels * 2 * 4)
        nn.Linear(64 * 3 * 3, h2),
        nn.ReLU(),
        
        # Output layer
        nn.Linear(h2, d_out),
        #nn.Softmax(dim=1)
    )

    dtype = torch.float

    use_cuda = torch.cuda.is_available()
    device = torch.device("cuda:0" if use_cuda else "cpu")
    print("Device:", device)
    x = x_train
    print("X Shape:", x.size())
    y = y_labels
    print("Y Shape:", y.size())

    loss_array = torch.zeros(epochs, 1)
    tick = datetime.now()

    #loss_function = torch.nn.MSELoss(reduction = 'sum')
    loss_function = torch.nn.CrossEntropyLoss()
    optimizer = optimizer_pick(1, net_model, alpha)

    epoch_count = 0

    for epoch in range(epochs):
        batch_count = 0
        for i, data in enumerate(train_loader, 1):
            inputs, targets = data
            inputs = inputs.float()

            y_pred = net_model((inputs).float())

            loss = loss_function(y_pred, targets)
            time = str(datetime.now())
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            batch_count += 1

        loss_array[epoch] = loss.item()

        print(f"Epoch {epoch + 1}/{epochs} completed. Loss: {loss.item():.10f}")
        epoch_count += 1

        # stops neural network if error rate is lower than desired
        if loss.item() < 1e-10:
            print(datetime.now(), "Loss for epoch: ", epoch, loss.item())
            input("Press Enter to Continue...")
            break

    torch.save(net_model.state_dict(), 'params.pt')
    tock = datetime.now()
    delta_time = tock - tick
    print("\nDone with general training. Total time: ", delta_time)
    print("\nStarting dataset testing...")

    for i in range(len(x_file_list)):
        x_test = x_file_list[i]
        y_test_file = y_file_list[i]

        x_test_loaded = np.load(x_test)
        
        # --- Removed transpose operation ---
        x_test_loaded = torch.from_numpy(x_test_loaded).float()

        y_test_loaded = np.load(y_test_file)
        
        # --- Removed transpose operation ---
        y_test_labels = torch.from_numpy(y_test_loaded).long().flatten() # Flatten for easier comparison
        
        y_test_pred = net_model(x_test_loaded)
        
        # Get the predicted class index for each sample
        predicted_classes = torch.argmax(y_test_pred, dim=1)

        # Move to numpy for file operations
        predicted_numpy = predicted_classes.numpy()
        packet_choice(predicted_numpy)
        
        accuracy(predicted_classes, y_test_labels)

def accuracy(predictions, y_test):
    # This is a much more efficient way to calculate accuracy
    correct_predictions = (predictions == y_test).sum().item()
    total = y_test.size(0)

    print("\nTotal Predictions:", total, "Accuracy Count:", correct_predictions)
    print("\nAccuracy of Predictions:", correct_predictions / total, "\n")

# This provides an optimizer for the machine learning algorithm
def optimizer_pick(choice, net_model, alpha):
    optimizer = torch.optim.Adam(net_model.parameters(), lr=alpha)
    return optimizer
