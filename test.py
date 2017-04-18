#!bin/bash/python
print("hello world")
import numpy as np
import pandas as pd

train_set = pd.read_csv('/Users/michaelsanders/datasets/Project4/train.csv')
train_set.columns
train_set.dtypes

train_set.AddressAccuracy.head()