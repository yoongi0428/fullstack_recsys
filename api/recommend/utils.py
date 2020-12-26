import numpy as np
import scipy.sparse as sp
from tqdm import tqdm

def load_rating_matrix_from_db(users, interactions):
    all_users = users.query.all()
    all_interactions = interactions.query.all()

    users = []
    items = []
    ratings = []

    for interaction in tqdm(all_interactions, total=len(all_interactions)):
        user_id = interaction.user.id
        movie_id = interaction.movie.id
        rating = interaction.rating

        users.append(user_id)
        items.append(movie_id)
        ratings.append(1)   # implicit

    rating_matrix = sp.csr_matrix((ratings, (users, items)))
    return rating_matrix

def split_train_test(rating_matrix, test_ratio=0.1, shape=None):
    if shape is None:
        shape = rating_matrix.shape
    num_users, num_items = shape
    train_data = {'users': [], 'items': [], 'ratings': []}
    test_data = {'users': [], 'items': [], 'ratings': []}
    for u in range(num_users):
        # u_items = rating_matrix[u].indices
        u_items = rating_matrix.indices[rating_matrix.indptr[u]: rating_matrix.indptr[u+1]]
        # u_ratings = rating_matrix[u].values
        num_test = int(len(u_items) * test_ratio)
        test_idx = np.random.choice(list(range(len(u_items))), size=num_test)
        for i in range(len(u_items)):
            if i in test_idx:
                test_data['users'].append(u)
                test_data['items'].append(i)
                test_data['ratings'].append(1.0)
            else:
                train_data['users'].append(u)
                train_data['items'].append(i)
                train_data['ratings'].append(1.0)
    train_matrix = sp.csr_matrix((train_data['ratings'], (train_data['users'], train_data['items'])), shape=shape)
    test_matrix = sp.csr_matrix((test_data['ratings'], (test_data['users'], test_data['items'])), shape=shape)
    return train_matrix, test_matrix    