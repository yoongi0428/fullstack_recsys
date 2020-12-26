import os
import math
import random
import pickle
import argparse

import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import scipy.sparse as sp
from sklearn.model_selection import train_test_split

from models import EASE

def evaluate(prediction, target_dict, top_k=10):
    relevant_items_partition = (-prediction).argpartition(top_k, 1)[:, 0:top_k]
    
    # top_k item score (not sorted)
    relevant_items_partition_original_value = np.take_along_axis(prediction, relevant_items_partition, 1)
    
    # top_k item sorted index for partition
    relevant_items_partition_sorting = np.argsort(-relevant_items_partition_original_value, 1)
    
    # sort top_k index
    recommendation = np.take_along_axis(relevant_items_partition, relevant_items_partition_sorting, 1)

    prec, recall, ndcg = 0.0, 0.0, 0.0
    for rec, uid in zip(recommendation, target_dict):
        tar = target_dict[uid]
        num_target_items = len(tar)

        if num_target_items == 0:
            continue

        hits_k = [(i + 1, item) for i, item in enumerate(rec) if item in tar]
        num_hits = len(hits_k)

        idcg_k = 0.0
        for i in range(1, min(num_target_items, top_k) + 1):
            idcg_k += 1 / math.log(i + 1, 2)

        dcg_k = 0.0
        for idx, item in hits_k:
            dcg_k += 1 / math.log(idx + 1, 2)
        
        prec_k = num_hits / top_k
        recall_k = num_hits / num_target_items
        ndcg_k = dcg_k / idcg_k

        prec += prec_k / len(recommendation)
        recall += recall_k / len(recommendation)
        ndcg += ndcg_k / len(recommendation)
    
    return {f'Prec@{top_k}': prec, f'Recall@{top_k}': recall, f'NDCG@{top_k}': ndcg}


parser = argparse.ArgumentParser()
parser.add_argument('--model', type=str, default='EASE')
parser.add_argument('--datafile', type=str, default='data/ml-100k/ml-100k.pkl')
parser.add_argument('--save_dir', type=str, default='models/ckpt')
parser.add_argument('--seed', type=int, default=12345)
args = parser.parse_args()

random.seed(args.seed)
np.random.seed(args.seed)
torch.random.manual_seed(args.seed)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(args.seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

if __name__ == '__main__':
    with open(args.datafile, 'rb') as f:
        data = pickle.load(f)
    
    train_matrix = data['train_matrix']
    target_dict = data['target_dict']
    user_dict = data['user_dict']
    item_dict = data['item_dict']

    target_new_dict = {user_dict[u]: target_dict[u] for u in target_dict}
    
    # build model
    # fit and save model offline
    if args.model == 'EASE':
        model = EASE(reg=1000)
        model.fit(train_matrix, args.save_dir)
    else:
        raise NotImplementedError('Model not currently available!')

    prediction = model.predict(train_matrix)
    print(evaluate(prediction, target_new_dict, 10))