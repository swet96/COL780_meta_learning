# -*- coding: utf-8 -*-
"""models.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1aXWrTOMr770PXcbYk7gRxdGmvPswzNET

# Deep Learning Models etc
"""

# Commented out IPython magic to ensure Python compatibility.

# !pip install import_ipynb --quiet
# from google.colab import drive #TODO
# drive.mount('/content/drive') #TODO
# %ls drive/MyDrive/'Colab Notebooks'

# !cp drive/MyDrive/'Colab Notebooks'/Meta_Learning_hw1/models.ipynb .
# !cp drive/MyDrive/'Colab Notebooks'/Meta_Learning_hw1/course_data.ipynb .
# !cp drive/MyDrive/'Colab Notebooks'/Meta_Learning_hw1/nb0.ipynb .
# !cp drive/MyDrive/'Colab Notebooks'/Meta_Learning_hw1/utils.ipynb .

from IPython.display import HTML
import import_ipynb   #why error, already installed in anothe rnotebook?
import random
import utils
utils.hide_toggle('Imports 1')

import numpy as np
import torch
from torch import nn
from torch import optim
from IPython import display
utils.hide_toggle('Imports 2')

"""Compute accuracy of predictions."""

def accuracy(Net,X_test,y_test,verbose=True):
    Net.eval()
    m = X_test.shape[0]
    y_pred = Net(X_test)
    predicted = torch.max(y_pred, 1)[1]
    correct = (predicted == y_test).float().sum().item()
    if verbose: print(correct,m)
    accuracy = correct/m
    Net.train()
    return accuracy
utils.hide_toggle('Function: accuracy')

def accuracy_variable(Net,data):
    step=0
    acc=0
    for (X,y) in data:
            y_pred = Net(X)
            step+=1
            acc+=accuracy(Net,X,y,verbose=False)
    a = acc/step
    return a

"""Generic training loop"""

def Train(Net,data,epochs=20,lr=5e-2,Loss=nn.NLLLoss(),verbose=False):
  Net.train()
  losses = []
  accs = []
  total_step=len(data)

  flag=True
  for epoch in range(epochs):

    for batch_idx, (x, y) in enumerate(data):
      out = Net(x)
    #   if flag==True: 
    #     # print("shape of X in batch: ",x.shape)
    #     print("shape of true y: ",y)
    #     print("shape of predicted y: ",out)
    #     flag=False
      
      loss = Loss(out, y)
      losses.append(loss)

      Net.optimizer.zero_grad() 
      loss.backward()
      Net.optimizer.step()
      accs.append(accuracy(Net, x, y, verbose=verbose))
      if (batch_idx+1) % 25 == 0:
            print ('Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}' 
                   .format(epoch+1, epochs, batch_idx+1, total_step, loss.item()))
  return Net,losses,accs



# ### INSERT YOUR CODE HERE
  # losses=[]
  # accs=[]
  # for param in Net.parameters():
  #   param.requires_grad = True

  # for epoch in range(epochs):
  #   for batch_idx, (X,y) in enumerate(data):
  #     # output = Net(X)
  #     # loss   = Loss(output,y)
  #     # losses.append(loss)

  #     # Net.optimizer.zero_grad()
  #     # loss.backward()

  #     # Net.optimizer.step()


  #     # acc=accuracy(Net,X,y,verbose=False)
  #     # accs.append(acc)
  # return Net,losses,accs


utils.hide_toggle('Function Train')



"""Multi-layer perceptron with ReLU non-lineartities; for classification or regression."""

# class MLP(nn.Module):
#   def __init__(self,dims,task='classification',lr=1e-3):   #TODO ASK SUBRAT: why 'task' is there?
#       super(MLP,self).__init__()
#       # Neural network layers assigned as attributes of a Module subclass
#       # have their parameters registered for training automatically.
#       ### INSERT YOUR CODE HERE
#       self.mlp=nn.Sequential(nn.Linear(dims[0],dims[1]),nn.ReLU(),nn.Linear(dims[1],dims[2]),nn.ReLU(),nn.Linear(dims[2],dims[3]))
      
#       # (nn.Layer(dims[i],dims[i+1]),nn.Relu()) for i in range(dims-1)
#       self.optimizer = optim.Adam(self.parameters(),lr=lr)

#   def forward(self,x):
#       ### Insert your code here
#       result=self.mlp(x)
#       return(x)


class MLP(nn.Module):
    def __init__(self,dims=[5,3,2],task='classification',lr=1e-3):
        super(MLP,self).__init__()
        # Neural network layers assigned as attributes of a Module subclass
        # have their parameters registered for training automatically.
        ### INSERT YOUR CODE HERE
        modules = []
        for i in range(len(dims)-2):
          modules.append(nn.Linear(dims[i], dims[i+1]))
          modules.append(nn.ReLU())

        modules.append(nn.Linear(dims[i+1], dims[i+2]))
        modules.append(nn.LogSoftmax())
        
        self.model = nn.Sequential(*modules)
        self.optimizer = optim.Adam(self.parameters(),lr=lr)
    
    def forward(self,x):
        ### Insert your code here
        x = self.model(x)
 
        return(x)
utils.hide_toggle('Class MLP')

"""Recurrent network using GRU"""

class SimpleRNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size,lr):
        # This just calls the base class constructor
        super().__init__()
        # Neural network layers assigned as attributes of a Module subclass
        # have their parameters registered for training automatically.
        self.input_size=input_size
        self.rnn = torch.nn.RNN(input_size,hidden_size, nonlinearity='relu', batch_first=True)
        self.linear = torch.nn.Linear(hidden_size,output_size)
        self.logsoft = nn.LogSoftmax(dim=-1)
        self.optimizer = optim.Adam(self.parameters(),lr=lr)
        self.flag=True

    def forward(self, x):
        # torch.nn.RNN also returns its hidden state but we don't use it.
        # While the RNN can also take a hidden state as input, the RNN
        # gets passed a hidden state initialized with zeros by default.
        # print("x: ",x.shape)
        if self.input_size==1: x=x.unsqueeze(-1)
        # print("After Unsqueezed: ", x.shape)

        ### INSERT YOUR CODE HERE
        # print(x.shape)
        x,h=self.rnn(x)
        # print(x.shape)
        # print("x: ", torch.Tensor.size(x), "h:", torch Tensor.size(h))
        x=self.linear(x)
        x=self.logsoft(x)
        x=x[:,-1,:]
        return x

class SimpleLSTM(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, lr):
        super().__init__()
        ### INSERT YOUR CODE HERE
        self.input_size=input_size
        self.lstm=torch.nn.LSTM(input_size,hidden_size)
        self.linear = torch.nn.Linear(hidden_size,output_size)
        self.logsoft = nn.LogSoftmax(dim=-1)
        self.optimizer = optim.Adam(self.parameters(),lr=lr)
        
    def forward(self, x):
        if self.input_size==1: x=x.unsqueeze(-1)

        # print("x(After unsqueezing): ", x.shape)
        #### INSERT YOUR CODE HERE
        x,c = self.lstm(x)
        x=self.linear(x)
        x=self.logsoft(x)
        x=x[:,-1,:]
        # print("x: ", x.shape)
        return x


class CNN_1D(nn.Module):

    def __init__(self,num_classes,lr, data, in_channels):
        super().__init__()

        self.data=data
        self.in_channels=in_channels
        self.conv1 =nn.Conv1d(in_channels,4,kernel_size=3) 
        self.conv2 =nn.Conv1d(4,8,kernel_size=3)
        
        if self.data=="sin": 
            self.fc1=nn.Linear(128,num_classes)
        elif self.data=="fin":
            self.pool=nn.AdaptiveAvgPool1d(10)
            self.fc1=nn.Linear(80,num_classes)
        
        self.relu=nn.ReLU()
        self.logsoft = nn.LogSoftmax()
        self.optimizer = optim.Adam(self.parameters(),lr=lr)

    def forward(self, x):
        if self.data=="sin":  
            x=x.unsqueeze(1)
        elif self.data=="fin":
            x=torch.permute(x,(0,2,1))
        
        x=self.conv1(x)
        x=self.relu(x)
        x=self.conv2(x)
        x=self.relu(x)
        if self.data=="fin":
            x=self.pool(x)
        # print(x.shape)
        x=x.reshape(x.shape[0],-1)  #(batch_size, -)

        x=self.fc1(x)
        x=self.logsoft(x)
        # x=nn.Softmax(x) #nn.CrossEntropyLoss() already does the sofmax transformation, so do not do it here again
        return x


class CNN_2D(nn.Module):

    def __init__(self,mod_size, in_channels, num_classes, lr):
        super().__init__()

        self.in_channels=in_channels
        self.mod_size   =(-1,1,mod_size[0],mod_size[1])
        
        self.conv1    = nn.Conv2d(in_channels=1, out_channels=8, kernel_size=3) 
        self.conv2    = nn.Conv2d(in_channels=8,out_channels=32, kernel_size=3)
        # self.conv3    = nn.Conv2d(in_channels=64,out_channels=128, kernel_size=3)
        self.pool     = nn.MaxPool2d(kernel_size=2)
        if mod_size[0]==28:
            self.fc1      = nn.Linear(800,num_classes) # 1 conv layer= 676 #2 conv layer= 8*5*5 # 3 conv layer=16
        elif mod_size[0]==20:
            self.fc1      = nn.Linear(288,num_classes) 
        self.relu     = nn.ReLU()
        self.logsoft  = nn.LogSoftmax(dim=1)
        self.optimizer= optim.Adam(self.parameters(),lr=lr)
        
    def forward(self,x):
        
        x=x.reshape(self.mod_size)
        # print("x: ", x.shape)
        x=self.conv1(x)
        x=self.relu(x)
        x=self.pool(x)

        x=self.conv2(x)
        x=self.relu(x)
        x=self.pool(x) #torch.Size([2, 8, 5, 5])

        # x=self.conv3(x)
        # x=self.relu(x)
        # x=self.pool(x) 

        x=x.reshape(x.shape[0],-1) # (batch_size, -)
        # print("x:(before fully) ", x.shape)
        x=self.fc1(x)
        x=self.logsoft(x)
        # x=nn.Softmax(x) #nn.CrossEntropyLoss() already does the sofmax transformation, so do not do it here again if using this loss function
        return x


class Transformer(nn.Module):
    def __init__(self, num_classes, lr, data):
        super().__init__()
        self.data=data
        
        if self.data=="sin": 
            encoder_layer = nn.TransformerEncoderLayer(d_model=20, nhead=10, batch_first=True)
            self.fc1=nn.Linear(20,num_classes)
        elif self.data=="fin":
            encoder_layer = nn.TransformerEncoderLayer(d_model=149, nhead=149, batch_first=True)
            self.pool=nn.AdaptiveAvgPool1d(10)
            self.fc1=nn.Linear(70,num_classes)
        self.transformer_encoder = nn.TransformerEncoder(encoder_layer, num_layers=6)
        self.logsoft = nn.LogSoftmax(dim=-1)
        self.optimizer = optim.Adam(self.parameters(),lr=lr)

    def forward(self,x):
        if self.data=="sin":  
            x=x.unsqueeze(1)
        # elif self.data=="fin":
        #     x=torch.permute(x,(0,2,1))

        
        # print("before encoding: ",x.shape)
        x=self.transformer_encoder(x)
        if self.data=="fin": 
            x=self.pool(x)
        x=x.reshape(x.shape[0],-1)
        print(x.shape)
        x=self.fc1(x)
        x=self.logsoft(x)

        # if self.data=="sin":  
        #     x=x.unsqueeze(1)
        return x





# class CNN_2D(nn.Module):

#     def __init__(self,mod_size, in_channels, num_classes, lr):
#         super().__init__()

#         self.in_channels=in_channels
#         self.mod_size   =(-1,1,mod_size[0],mod_size[1])
        
#         self.conv1    = nn.Conv2d(in_channels=1, out_channels=4, kernel_size=3) 
#         self.conv2    = nn.Conv2d(in_channels=4,out_channels=8, kernel_size=3)
#         self.conv3    = nn.Conv2d(in_channels=8,out_channels=16, kernel_size=3)
#         self.pool     = nn.MaxPool2d(kernel_size=2)
#         self.adaptive_pool=nn.AdaptiveAvgPool2d()
#         self.fc1      = nn.Linear(16*5*5,num_classes)
#         self.relu     = nn.ReLU()
#         self.logsoft  = nn.LogSoftmax()
#         self.optimizer= optim.Adam(self.parameters(),lr=lr)
        
#     def forward(self,x):
        
#         x=x.reshape(self.mod_size)
#         # print("x: ", x.shape)
#         x=self.conv1(x)
#         x=self.relu(x)
#         x=self.pool(x)
#         x=self.conv2(x)
#         x=self.relu(x)
#         x=self.pool(x) #torch.Size([2, 8, 5, 5])
#         x=self.conv3(x)
#         x=self.relu(x)
#         x=self.pool(x) 
#         x=x.reshape(x.shape[0],-1) # (batch_size, -)
#         # print("x:(before fully) ", x.shape)
#         x=self.fc1(x)
#         x=self.logsoft(x)
#         # x=nn.Softmax(x) #nn.CrossEntropyLoss() already does the sofmax transformation, so do not do it here again
#         return x


