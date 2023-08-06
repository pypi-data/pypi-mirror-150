import pandas as pd
import torch
import torch.nn.functional as F
import numpy as np


class Fairness(object):

    def __init__(self, pandas_df):
        self.test = pandas_df

    def new_test(self, column_name=None):
        value_list = self.test[column_name].drop_duplicates().to_list()
        self.test[column_name] = self.test[column_name].\
            apply(lambda x:value_list[np.random.randint(0, len(value_list))])

    def compe(self, x, y):
        kl = F.kl_div(x.softmax(dim=-1).log(), y.softmax(dim=-1), reduction='sum')
        return kl
#
# F = Fairness('./test_model/test.csv')
# print(F.test['Sex'].value_counts())
# F.new_test("Sex")
# print(F.test['Sex'].value_counts())
#
# def fairness(column_name=None):
#     pdf = pd.read_csv
#     value = pd[column_name]
#     # x = torch.Tensor(result['Survived'].to_list())
#     # y = torch.Tensor(new_result['Survived'].to_list())
#     # kl = F.kl_div(x.softmax(dim=-1).log(), y.softmax(dim=-1), reduction='sum')
#     # return kl



