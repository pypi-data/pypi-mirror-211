from __future__ import division
from __future__ import print_function

import time
import numpy as np
import random
import torch
import torch.nn.functional as F

from .model import MXMNet, Config
import pandas as pd
import matplotlib.pyplot as plt
from torch_geometric.loader import DataLoader
import copy
from sklearn.metrics import r2_score
import os

os.environ['CUDA_LAUNCH_BLOCKING'] = '1'
# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# if torch.cuda.is_available():
#     torch.cuda.set_device(0)
device = torch.device('cpu')


data_path = '../data/data_chang.pt'
result_path = '../predict_result/data_chang.txt'
csv_path = '../predict_result/date_chang.csv'

# 把想用的模型复制predict文件夹下
model_path = 'model.pt'
f = open(result_path, 'w', encoding='utf-8')


dataset = torch.load(data_path)
print("test samples num: ", len(dataset), file=f)
print(dataset[0], file=f)

test_loader = DataLoader(dataset, batch_size=1, shuffle=False, drop_last=True)

config = Config(dim=128, n_layer=6, cutoff=5.0)
model = MXMNet(config).to(device)

model.load_state_dict(torch.load(model_path))
print('load model from {}'.format(model_path), file=f)

model.eval()
smiles_ls= []
pred_ls = []
name_ls = []
# y_ls = []
for batch in test_loader:
    batch = batch.to(device)
    with torch.no_grad():
        print(batch.smiles)
        pred_ls.append(model(batch))
        # y_ls.append(batch.y)
        smiles_ls += batch.smiles
        name_ls += batch.filename

pred = torch.cat(pred_ls, dim=0).reshape(-1)
# y = torch.cat(y_ls, dim=0).reshape(-1)

# mae = F.l1_loss(pred.reshape(-1), y.reshape(-1))
# test_loss = mae
# rmse = torch.sqrt(test_loss)

# r_2 = r2_score(y.cpu().numpy(), pred.cpu().numpy())
# ratio_02 = (torch.abs(y - pred) <= 0.2).sum() / y.size(0)
# ratio_01 = (torch.abs(y - pred) <= 0.1).sum() / y.size(0)

# print('MSE: {:.8f}'.format(test_loss), file=f)
# print('RMSE: {:.8f}'.format(rmse), file=f)
# print('MAE: {:.8f}'.format(mae), file=f)
# print('R_2: {:.5f}'.format(r_2), file=f)
# print('Ratio_02: {:.5f}'.format(ratio_02), file=f)
# print('Ratio_01: {:.5f}'.format(ratio_01), file=f)
# print('#' * 40, file=f)

f.close()

pred_data = {
    'name': name_ls,
    'smiles': smiles_ls,
    # 'y': y.cpu().tolist(),
    'pred': pred.cpu().tolist(),
}
pred_df = pd.DataFrame(pred_data)
pred_df['pred'] = pred_df['pred'].apply(lambda x: round(x, 2))
pred_df.to_csv(csv_path, index=False)
def main():
    print("this is my library")
if __name__ == '__main__':
    main()

