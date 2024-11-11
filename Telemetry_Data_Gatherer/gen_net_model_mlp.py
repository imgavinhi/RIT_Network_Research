import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.data as data_utils

from datetime import datetime
import os.path

#defines the main operations for the machine learning neaural network
def gen_net_mlp_main(x_train, y_labels, x_file_list, y_file_list, feature_count, iterations, hidden_nodes, classes, alpha, batch_size):
    d_in = feature_count
    print(d_in)
    print(type(d_in))
    h2 = hidden_nodes
    h1 = hidden_nodes #typically *2

    iteration_ctr = 0
    d_out = classes
    epochs = iterations

    max_tier = 20
    train = data_utils.TensorDataset(x_train, y_labels)
    train_loader = data_utils.DataLoader(train, batch_size=batch_size, shuffle=False)

    net_model = torch.nn.Sequential(
            torch.nn.Linear(int(d_in.shape[0]), h1),
            torch.nn.ReLU(),
            torch.nn.Linear(h1, h2),
            torch.nn.ReLU(),
            torch.nn.Linear(h1, h2),
            torch.nn.ReLU(),
            torch.nn.Linear(h2, d_out),
            torch.nn.Softmax(dim=1)
    )

    dtype = torch.float

    use_cuda = torch.cuda.is_available()
    device = torch.device("cuda:0" if use_cuda else "cpu")
    x = x_train
    y = y_labels

    loss_array = torch.zeros(epochs, 1)
    tick = datetime.now()

    loss_function = torch.nn.MSELoss(reduction = 'sum')
    optimizer = optimizer_pick(1, net_model, alpha)

    epoch_count = 0

    for epoch in range(epochs):
        batch_count = 0
        for i, data in enumerate(train_loader, 1):
            inputs, targets = data
            inputs = inputs.float()

            y_pred = net_model((inputs).float())

            loss = loss_function(y_pred, targets.float())
            time = str(datetime.now())
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            batch_count += 1

        loss_array[epoch] = loss.item()

        epoch_count += 1

        #stops neural network if error rate is lower than desired
        if loss.item() < 1e-8:
            print(datetime.now(), "Loss for epoch: ", epoch, loss.item())
            break

    torch.save(net_model.state_dict(), 'params.pt')
    tock = datetime.now()
    delta_time = tock - tick
    print("\nDone with general training. Total time: ", delta_time)
    print("\nStarting dataset testing...")

    for i in range(len(x_file_list)):
        x_test = x_file_list[i]
        y_test = y_file_list[i]

        x_test = np.load(x_test)
        x_test = np.transpose(x_test)
        x_test = torch.from_numpy(x_test).float()

        y_test = np.load(y_test)
        y_test = np.transpose(y_test)
        y_test = torch.from_numpy(y_test)
        y_test_labels = torch.zeros(x_test.shape[0], classes)

        y_test_pred = net_model(x_test)

        predicted = torch.zeros(x_test.shape[0])

        for j in range(x_test.shape[0]):
            place = torch.argmax(y_test_pred[j])

            predicted[j] = place
        
        predicted_numpy = predicted.numpy()
        # this is from "predictions" maybe substitute with my "statistics" packet_choice()
        
        accuracy(predicted_numpy, y_test)

def accuracy(predictions, y_test):
    accuracy_count = 0
    total  = predictions.shape[0]
    for i in range(predictions.shape[0]):
        if int(predictions[i]) == int(y_test[0][i]):
            accuracy_count += 1

    print("\nTotal Predictions:", total, "Accuracy Count:", accuracy_count)
    print("\nAccuracy of Predictions:", accuracy_count/total)

#This provides an optimizer for the machine learning algorithm, "Everyone cchooses Adam" --Hartpence
def optimizer_pick(choice, net_model, alpha):
    optimizer = torch.optim.Adam(net_model.parameters(), lr=alpha)
    return optimizer

