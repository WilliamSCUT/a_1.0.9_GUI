import torch
from torch._C import set_flush_denormal
import torch.nn.functional as F
import numpy as np

class Predator_nn(torch.nn.Module):

    def __init__(self, n_input, n_hidden, n_output):
        super(Predator_nn, self).__init__()
        # self.n_input = n_input #16
        # self.n_hidden = n_hidden #32
        # self.n_output = n_output #4
        
        self.hidden1 = torch.nn.Linear(n_input, n_hidden)
        self.hidden2 = torch.nn.Linear(n_hidden,n_hidden)
        self.predict = torch.nn.Linear(n_hidden,n_output)

    def forward(self, input_data):
        out = torch.sigmoid(input_data)
        out = self.hidden1(out)
        out = torch.sigmoid(out)
        out = self.hidden2(out)
        out = torch.sigmoid(out)
        out = self.predict(out)
        out = F.softmax(out,dim=1)
        
        return out