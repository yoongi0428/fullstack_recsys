import os
import math
from time import time
from tqdm import tqdm

import numpy as np
import torch
import torch.nn as nn
import scipy.sparse as sp

from base import BaseRecommender
from dataloader.DataBatcher import DataBatcher

class ItemKNN(BaseRecommender):
    def __init__(self, dataset, model_conf, device):
        super(ItemKNN, self).__init__(dataset, model_conf)
        """
        * cosine
            - normalize: T/F
        * asymetric cosine
            - normalize: T/F
            - asymmetric_alpha
        * tanimoto (jaccard)
            - normalize: F
        * dice
            - normalize: F
        * tversky
            - normalize: F
            - tversky alpha
            - tversky beta
        """
        self.dataset = dataset
        self.num_users = dataset.num_users
        self.num_items = dataset.num_items
        self.top_k = model_conf['top_k']
        self.shrink = model_conf['shrink']
        self.similarity = model_conf['similarity']
        self.feature_weighting = model_conf['feature_weighting']
        assert self.feature_weighting in ['tf-idf', 'bm25', 'none']

        # Asymetric
        self.asymmetric_alpha = model_conf['asymmetric_alpha']
        # tversky
        self.tversky_alpha = model_conf['tversky_alpha']
        self.tversky_beta = model_conf['tversky_beta']

        self.positive_only=True

        self.device = device

    def train_model(self, dataset, evaluator, early_stop, neptune, logger, config, neptune_prefix=''):
        log_dir = logger.log_dir

        train_matrix = dataset.train_matrix
        if self.feature_weighting == 'tf-idf':
            train_matrix = self.TF_IDF(train_matrix.T).T
        elif self.feature_weighting == 'bm25':
            train_matrix = self.okapi_BM25(train_matrix.T).T
        train_matrix = train_matrix.tocsc()
        num_items = train_matrix.shape[1]

        start_col_local = 0
        end_col_local = num_items

        start_col_block = start_col_local

        this_block_size = 0
        block_size = 500

        
        start = time()

        sumOfSquared = np.array(train_matrix.power(2).sum(axis=0)).ravel()
        if self.similarity == 'cosine' or self.similarity == 'asymmetric_cosine':
            sumOfSquared = np.sqrt(sumOfSquared)

        if self.similarity == 'asymmetric_cosine':
            sumOfSquared_to_1_minus_alpha = np.power(sumOfSquared, 2 * (1 - self.asymmetric_alpha))
            sumOfSquared_to_alpha = np.power(sumOfSquared, 2 * self.asymmetric_alpha)

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

                # Apply normalization and shrinkage, ensure denominator != 0
                if self.similarity == 'cosine':
                    # cosine similarity
                    # denominator = sqrt(l2_norm(x)) * sqrt(l2_norm(y))+ shrinkage + eps
                    denominator = sumOfSquared[columnIndex] * sumOfSquared + self.shrink + 1e-6
                    this_column_weights = np.multiply(this_column_weights, 1 / denominator)

                elif self.similarity == 'asymmetric_cosine':
                    denominator = sumOfSquared_to_alpha[columnIndex] * sumOfSquared_to_1_minus_alpha + self.shrink + 1e-6
                    this_column_weights = np.multiply(this_column_weights, 1 / denominator)
                    
                # Apply the specific denominator for Tanimoto
                elif self.similarity == 'tanimoto':
                    # denominator = sqrt(l2_norm(x)) + sqrt(l2_norm(y)) - xy + shrinkage + eps
                    denominator = sumOfSquared[columnIndex] + sumOfSquared - this_column_weights + self.shrink + 1e-6
                    this_column_weights = np.multiply(this_column_weights, 1 / denominator)

                elif self.similarity == 'dice':
                    # denominator = sqrt(l2_norm(x)) + sqrt(l2_norm(y)) + shrinkage + eps
                    denominator = sumOfSquared[columnIndex] + sumOfSquared + self.shrink + 1e-6
                    this_column_weights = np.multiply(this_column_weights, 1 / denominator)

                elif self.similarity == 'tversky':
                    # denominator = xy + (sqrt(l2_norm(x)) - xy) * alpha + (sqrt(l2_norm(y)) - xy) * beta + shrinkage + eps
                    denominator = this_column_weights + \
                                    (sumOfSquared[columnIndex] - this_column_weights)*self.tversky_alpha + \
                                    (sumOfSquared - this_column_weights)*self.tversky_beta + self.shrink + 1e-6
                    this_column_weights = np.multiply(this_column_weights, 1 / denominator)

                # If no normalization or tanimoto is selected, apply only shrink
                elif self.shrink != 0:
                    # denominator = shrinkage
                    print('No normalization, only shrinkage')
                    this_column_weights = this_column_weights / self.shrink


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
        sp.save_npz(os.path.join(log_dir, 'best_model'), self.W_sparse)

        valid_score = evaluator.evaluate(self)
        if neptune is not None:
            valid_neptune_dict = {neptune_prefix + k: v for k,v in valid_score.items()}
            neptune.log_metric_from_dict(valid_neptune_dict, epoch=1)

        total_train_time = time() - start

        return valid_score, total_train_time

    def predict(self, user_ids, eval_pos_matrix, eval_items=None):
        batch_eval_pos = eval_pos_matrix[user_ids]

        # eval_pos_matrix
        eval_output = (batch_eval_pos * self.W_sparse).toarray()
        
        if eval_items is not None:
            eval_output[np.logical_not(eval_items)]=float('-inf')
        else:
            eval_output[batch_eval_pos.nonzero()] = float('-inf')

        return eval_output

    def restore(self, log_dir):
        self.W_sparse = sp.load_npz(os.path.join(log_dir, 'best_model.npz'))

    
    def okapi_BM25(self, dataMatrix, K1=1.2, B=0.75):
        assert B>0 and B<1, "okapi_BM_25: B must be in (0,1)"
        assert K1>0,        "okapi_BM_25: K1 must be > 0"


        # Weighs each row of a sparse matrix by OkapiBM25 weighting
        # calculate idf per term (user)

        dataMatrix = sp.coo_matrix(dataMatrix)

        N = float(dataMatrix.shape[0])
        idf = np.log(N / (1 + np.bincount(dataMatrix.col)))

        # calculate length_norm per document
        row_sums = np.ravel(dataMatrix.sum(axis=1))

        average_length = row_sums.mean()
        length_norm = (1.0 - B) + B * row_sums / average_length

        # weight matrix rows by bm25
        dataMatrix.data = dataMatrix.data * (K1 + 1.0) / (K1 * length_norm[dataMatrix.row] + dataMatrix.data) * idf[dataMatrix.col]

        return dataMatrix.tocsr()

    def TF_IDF(self, matrix):
        """
        Items are assumed to be on rows
        :param dataMatrix:
        :return:
        """

        # TFIDF each row of a sparse amtrix
        dataMatrix = sp.coo_matrix(matrix)
        N = float(dataMatrix.shape[0])

        # calculate IDF
        idf = np.log(N / (1 + np.bincount(dataMatrix.col)))

        # apply TF-IDF adjustment
        dataMatrix.data = np.sqrt(dataMatrix.data) * idf[dataMatrix.col]

        return dataMatrix.tocsr()