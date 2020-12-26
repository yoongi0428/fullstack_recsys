import os
import random
import pickle
import argparse

import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import scipy.sparse as sp
from sklearn.model_selection import train_test_split

parser = argparse.ArgumentParser()
parser.add_argument('--seed', type=int, default=12345)
args = parser.parse_args()

random.seed(args.seed)
np.random.seed(args.seed)
torch.random.manual_seed(args.seed)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(args.seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

def user_item_dict(df):
    unique_users = pd.unique(df['user']).tolist()
    user_id_dict = {x: i for i, x in enumerate(unique_users)}

    unique_items = pd.unique(df['item']).tolist()
    item_id_dict = {x: i for i, x in enumerate(unique_items)}
    
    return user_id_dict, item_id_dict

def convert_df_into_sp(df, user_id_dict, item_id_dict):
    num_users, num_items = len(user_id_dict), len(item_id_dict)

    row = [user_id_dict[x] for x in df['user'].values.tolist()]
    col = [item_id_dict[x] for x in df['item'].values.tolist()]
    # val = df['rating'].values.tolist()
    val = [1.0] * len(df)

    rating_matrix = sp.csr_matrix((val, (row, col)), shape=(num_users, num_items))
    return rating_matrix

def load_item_info(data_dir):
    info_file = os.path.join(data_dir, 'u.item')
    with open(info_file, 'rt', encoding="ISO-8859-1") as f:
        lines = f.readlines()
    
    genre_list = ['unknown', 'Action', 'Adventure' ,'Animation', 'Children\'s', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
    item_info_dict = {}
    for line in lines:
        line = line.strip().split('|')
        item_id = int(line[0])
        title = line[1]
        date = line[2]
        genre_mask = [int(x) for x in line[-19:]]
        genre_idx = np.nonzero(genre_mask)[0]
        genre = [genre_list[x] for x in genre_idx]

        item_info_dict[item_id] = {
            'title': title,
            'date': date,
            'genre': genre
        }
    return item_info_dict

def preprocess(filename, save_dir):
    # load dataset
    num_users = 943
    num_items = 1682
    
    item_dict = load_item_info('data/ml-100k')

    full_data = pd.read_csv(filename, delimiter='\t', names=['user', 'item', 'rating', 'timestamp'])
    user_id_dict, item_id_dict = user_item_dict(full_data)
    assert num_users == len(user_id_dict)
    assert num_items == len(item_id_dict)

    new_to_old = {new: old for old, new in user_id_dict.items()}

    for i in item_dict:
        item_dict[i]['new_id'] = item_id_dict[i]

    train_data, test_data = train_test_split(full_data, test_size=0.2, random_state=2021)

    train_matrix = convert_df_into_sp(train_data, user_id_dict, item_id_dict)
    test_matrix = convert_df_into_sp(test_data, user_id_dict, item_id_dict)
    target_dict = {new_to_old[u]: test_matrix[u].indices for u in range(num_users)}

    save_dict = {
        'train_matrix': train_matrix,
        'target_dict': target_dict,
        'user_dict': user_id_dict,
        'item_dict': item_dict
    }

    with open(os.path.join(save_dir, 'ml-100k.pkl'), 'wb') as f:
        pickle.dump(save_dict, f)

if __name__ == '__main__':
    preprocess(os.path.join('data', 'ml-100k', 'u.data'), os.path.join('data', 'ml-100k'))