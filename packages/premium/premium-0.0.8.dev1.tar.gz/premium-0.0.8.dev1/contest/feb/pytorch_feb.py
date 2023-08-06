from abc import abstractmethod
import os
import random
import time
from math import factorial
from typing import Any, Callable, NamedTuple

import codefast as cf
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import premium as pm
import torch
import torch.nn as nn
import torch.nn.functional as F
from scipy.stats import mode
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.utils.class_weight import compute_class_weight
from torch.utils.data import DataLoader, Dataset
from tqdm import tqdm

from data import DataLoader as ddl
from dofast import SyncFile
from typing import List, Tuple

class MyDataLoader(pm.AbstractDataLoader):
    def __init__(self, local_dir: str, remote_dir: str):
        files = ['train.csv', 'test.csv', 'sample_submission.csv']
        super().__init__(local_dir, remote_dir, files)

    def __call__(self, frac: float = 1.0):
        self.label_encoder = LabelEncoder()
        train, test, sub = [sf.read_csv().df for sf in self.syncfiles]
        features = [col for col in test.columns if 'row_id' not in col]
        train = train.drop_duplicates(subset=features).sample(
            frac=self.train_frac)
        labels = self.label_encoder.fit_transform(train['target'])
        train, test = train[features], test[features]
        print(train.head(), train.shape)
        return train, labels, test, sub


from torch.utils.data import DataLoader, Dataset


class CustomDataset(Dataset):
    def __init__(self, X, y) -> None:
        self.X = torch.tensor(X.values)
        self.y = torch.tensor(y)

    def __getitem__(self, index):
        return self.X[index], self.y[index]

    def __len__(self):
        return len(self.X)


class TestDataset(Dataset):
    def __init__(self, X):
        self.X = torch.tensor(X.values)

    def __getitem__(self, idx):
        return self.X[idx]

    def __len__(self):
        return len(self.X)


class ResidualBlock(nn.Module):
    def __init__(self, channel):
        super().__init__()
        self.fc = nn.Linear(channel, channel)

    def forward(self, x):
        y = F.relu(self.fc(x))
        y = self.fc(y)

        return F.relu(x + y)


class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv = nn.Sequential(nn.Linear(286, 512), nn.ReLU(),
                                  nn.BatchNorm1d(512), ResidualBlock(512),
                                  nn.Linear(512, 256), nn.ReLU(),
                                  nn.BatchNorm1d(256), ResidualBlock(256),
                                  nn.Linear(256, 128), nn.ReLU(),
                                  nn.BatchNorm1d(128), ResidualBlock(128),
                                  nn.Linear(128, 128), nn.ReLU(),
                                  nn.BatchNorm1d(128), ResidualBlock(128),
                                  nn.Linear(128, 64), nn.ReLU())
        self.fc = nn.Linear(64, 10)

    def forward(self, x):
        x = self.conv(x)
        x = self.fc(x)
        return x


mdl = MyDataLoader(local_dir='/tmp/tabular_2022_feb',
                   remote_dir='kaggle/tabular_2022_feb')
train, labels, test, sub = mdl(frac=1.0)
X_train, X_test, y_train, y_test = train_test_split(train,
                                                    labels,
                                                    test_size=0.2,
                                                    random_state=42)
train_set = CustomDataset(X_train, y_train)
test_set = CustomDataset(X_test, y_test)
pred_set = TestDataset(test)
# Device configuration
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
# Hyper parameters
num_epochs = 100
batch_size = 128
learning_rate = 0.0000588
train_loader = DataLoader(dataset=train_set,
                          batch_size=batch_size,
                          shuffle=True)
test_loader = DataLoader(dataset=test_set, batch_size=batch_size, shuffle=True)

ResNet_model = Net().to(device)
ResNet_criterion = nn.CrossEntropyLoss()
ResNet_optimizer = torch.optim.AdamW(ResNet_model.parameters(),
                                     lr=learning_rate)

ResNet_model.train()

step = len(train_loader) + len(test_loader)
for epoch in range(num_epochs):
    epoch_RNloss = 0

    for x, label in tqdm(train_loader):
        x = x.to(device)
        label = label.to(device)

        # Forward pass
        RNoutput = ResNet_model(x.float())
        RNloss = ResNet_criterion(RNoutput, label)
        epoch_RNloss += RNloss.item()

        # Backward and optimize
        ResNet_optimizer.zero_grad()
        RNloss.backward()
        ResNet_optimizer.step()

    for x, label in tqdm(test_loader):
        x = x.to(device)
        label = label.to(device)

        # Forward pass
        RNoutput = ResNet_model(x.float())
        RNloss = ResNet_criterion(RNoutput, label)
        epoch_RNloss += RNloss.item()

        # Backward and optimize
        ResNet_optimizer.zero_grad()
        RNloss.backward()
        ResNet_optimizer.step()

    print(
        f'Epoch:[{epoch + 1}/{num_epochs}], Average Loss in ResNet: {epoch_RNloss/step:.6f}'
    )

ResNet_model.eval()

true_label = []
pred_label = []
with torch.no_grad():
    for x, label in test_loader:
        x = x.to(device)
        label = label.to(device)
        outputs = ResNet_model(x.float())
        pred_label.extend(torch.argmax(outputs, axis=1).cpu().numpy())
        true_label.extend(label.cpu().numpy())

cf_mat = confusion_matrix(true_label, pred_label)
print(cf_mat)
clf_report = classification_report(true_label, pred_label, digits=4)
print(clf_report)

pred_loader = DataLoader(dataset=pred_set,
                         batch_size=batch_size,
                         shuffle=False)
pred_label = []
with torch.no_grad():
    for x in pred_loader:
        x = x.to(device)
        label = label.to(device)
        outputs = ResNet_model(x.float())
        pred_label.extend(torch.argmax(outputs, axis=1).cpu().numpy())
        true_label.extend(label.cpu().numpy())

sub.target = mdl.label_encoder.inverse_transform(pred_label)
print(sub.head())
sub.to_csv('submission.csv', index=False)

