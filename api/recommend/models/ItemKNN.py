import os
import math
from time import time
from tqdm import tqdm

import numpy as np
import scipy.sparse as sp

class ItemKNN:
    def __init__(self, top_k=100):
        self.top_k = top_k

    @property
    def save_filename(self):
        return f'ItemKNN_{self.top_k}'

    def fit(self, train_matrix, save_path):
        num_users, num_items = train_matrix.shape   
        train_matrix = train_matrix.tocsc()

        start_col_local = 0
        end_col_local = num_items

        start_col_block = start_col_local

        this_block_size = 0
        block_size = 500

        
        start = time()

        sumOfSquared = np.array(train_matrix.power(2).sum(axis=0)).ravel()
        sumOfSquared = np.sqrt(sumOfSquared)

        values = []
        rows = []
        cols = []
        while start_col_block < end_col_local:
            end_col_block = min(start_col_block + block_size, end_col_local)
            this_block_size = end_col_block-start_col_block

            # All data points for a given item
            # item_data: user, item blocks
            item_data = train_matrix[:, start_col_block:end_col_block]
            item_data = item_data.toarray().squeeze()

            # If only 1 feature avoid last dimension to disappear
            if item_data.ndim == 1:
                item_data = np.atleast_2d(item_data)

            # if self.use_row_weights:
            #     this_block_weights = self.dataMatrix_weighted.T.dot(item_data)

            # else:
            #     # Compute item similarities
            #     # (item, user) x (user, item blocks) = (item, item blocks)
            this_block_weights = train_matrix.T.dot(item_data)

            for col_index_in_block in range(this_block_size):
                # this_block_size: (item,)
                # similarity between 'one block item' and whole items
                if this_block_size == 1:
                    this_column_weights = this_block_weights
                else:
                    this_column_weights = this_block_weights[:,col_index_in_block]

                # columnIndex = item index
                # zero out self similarity
                columnIndex = col_index_in_block + start_col_block
                this_column_weights[columnIndex] = 0.0

                # cosine similarity
                # denominator = sqrt(l2_norm(x)) * sqrt(l2_norm(y))+ shrinkage + eps
                denominator = sumOfSquared[columnIndex] * sumOfSquared
                this_column_weights = np.multiply(this_column_weights, 1 / denominator)

                relevant_items_partition = (-this_column_weights).argpartition(self.top_k-1)[0:self.top_k]
                relevant_items_partition_sorting = np.argsort(-this_column_weights[relevant_items_partition])
                top_k_idx = relevant_items_partition[relevant_items_partition_sorting]

                # Incrementally build sparse matrix, do not add zeros
                notZerosMask = this_column_weights[top_k_idx] != 0.0
                numNotZeros = np.sum(notZerosMask)

                values.extend(this_column_weights[top_k_idx][notZerosMask])
                rows.extend(top_k_idx[notZerosMask])
                cols.extend(np.ones(numNotZeros) * columnIndex)

            start_col_block += block_size
        
        self.W_sparse = sp.csr_matrix((values, (rows, cols)),
                            shape=(num_items, num_items),
                            dtype=np.float32)
        # Save
        self.save(save_path)

    def predict(self, rating_matrix):
        input_matrix = rating_matrix
        eval_output = input_matrix @ self.W_sparse
        eval_output[rating_matrix.nonzero()] = float('-inf')

        return eval_output.toarray()
        
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
        sp.save_npz(os.path.join(save_dir, self.save_filename), self.W_sparse)

    def restore(self, ckpt):
        self.W_sparse = sp.load_npz(ckpt)
        print('restore:', self.W_sparse.shape)
        self.num_items = self.W_sparse.shape[0]