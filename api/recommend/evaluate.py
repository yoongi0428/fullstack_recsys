import math
import numpy as np

def extract_top_k(prediction, k):
    # top_k item index (not sorted)
    relevant_items_partition = (-prediction).argpartition(k, 1)[:, 0:k]
    
    # top_k item score (not sorted)    
    relevant_items_partition_original_value = np.take_along_axis(prediction, relevant_items_partition, 1)
    # top_k item sorted index for partition
    relevant_items_partition_sorting = np.argsort(-relevant_items_partition_original_value, 1)
    
    # sort top_k index
    topk = np.take_along_axis(relevant_items_partition, relevant_items_partition_sorting, 1)

    return topk

def evaluate(top_k, test_matrix, k):
    num_users = test_matrix.shape[0]
    score = {
        f'prec@{k}': 0.0,
        f'recall@{k}': 0.0,
        f'ndcg@{k}': 0.0
    }
    for u in range(num_users):
        u_target = test_matrix.indices[test_matrix.indptr[u]: test_matrix.indptr[u+1]]
        u_topk = top_k[u]
        num_target = len(u_target)

        hits_k = [(i + 1, item) for i, item in enumerate(u_topk) if item in u_target]
        num_hits = len(hits_k)

        idcg_k = 0.0
        for i in range(1, min(num_target, k) + 1):
            idcg_k += 1 / math.log(i + 1, 2)

        dcg_k = 0.0
        for idx, item in hits_k:
            dcg_k += 1 / math.log(idx + 1, 2)
        
        prec_k = num_hits / k
        recall_k = num_hits / num_target
        ndcg_k = dcg_k / idcg_k

        score[f'prec@{k}'] += prec_k / num_users
        score[f'recall@{k}'] += recall_k / num_users
        score[f'ndcg@{k}'] += ndcg_k / num_users
    return score