"""
Embarrassingly shallow autoencoders for sparse data, 
Harald Steck,
Arxiv.
"""
import os
import math
from time import time

import numpy as np

class EASE:
    def __init__(self, reg=100):
        self.reg = reg
        self.enc_w = None
    
    @property
    def save_filename(self):
        return f'EASE_{self.reg}'

    def fit(self, train_matrix, save_path):
        self.num_users, self.num_items = train_matrix.shape    
        users = list(range(self.num_users))

        G = train_matrix.T @ train_matrix
        diag = np.diag_indices(G.shape[0])
        G[diag] += self.reg
        P = np.linalg.inv(G.toarray())
        self.enc_w = P / (-np.diag(P))
        self.enc_w[diag] = 0

        # Save
        self.save(save_path)        

    def predict(self, rating_matrix):
        input_matrix = rating_matrix
        eval_output = input_matrix @ self.enc_w
        eval_output[rating_matrix.nonzero()] = float('-inf')

        return eval_output
    
    def recommend(self, user_context, top_k=10):
        user_vec = np.zeros((1, self.num_items))
        user_vec[0, user_context] = 1

        prediction = self.predict(user_vec)

        relevant_items_partition = (-prediction).argpartition(top_k, 1)[:, 0:top_k]
    
        # top_k item score (not sorted)
        relevant_items_partition_original_value = np.take_along_axis(prediction, relevant_items_partition, 1)
        
        # top_k item sorted index for partition
        relevant_items_partition_sorting = np.argsort(-relevant_items_partition_original_value, 1)
        
        # sort top_k index
        recommendation = np.take_along_axis(relevant_items_partition, relevant_items_partition_sorting, 1)

        return recommendation.reshape(-1).tolist()

    def save(self, save_dir):
        np.save(os.path.join(save_dir, self.save_filename), self.enc_w)

    def restore(self, ckpt):
        self.enc_w = np.load(ckpt)
        print('restore:', self.enc_w.shape)
        self.num_items = self.enc_w.shape[0]