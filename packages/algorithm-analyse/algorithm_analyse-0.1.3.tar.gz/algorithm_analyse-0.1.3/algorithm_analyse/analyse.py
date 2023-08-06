import pandas as pd
import torch
import torch.nn.functional as F
import numpy as np
import matplotlib.pyplot as plt


class Analyse(object):

    def __init__(self, pandas_df):
        self.test = pandas_df

    def new_test(self, column_name=None):
        value_list = self.test[column_name].drop_duplicates().to_list()
        self.test[column_name] = self.test[column_name].\
            apply(lambda x:value_list[np.random.randint(0, len(value_list))])

    def compare(self, x, y):
        kl = F.kl_div(x.softmax(dim=-1).log(), y.softmax(dim=-1), reduction='sum')
        return kl

    def dis_analyse(self, x, y):
        self.test.plot.scatter(x, y)
        plt.show()

    def completeness(self, x):
        result = self.test[x].isnull().sum(axis=0)
        return result

