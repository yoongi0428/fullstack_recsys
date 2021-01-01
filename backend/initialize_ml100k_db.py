import os
from tqdm import tqdm
import argparse
import numpy as np
import pandas as pd
from datetime import datetime
from app import db
from app.model import Movie, User, Interaction


# Load file, generate id map, update users & movies, update interactions

def load_user_info(info_file):
    with open(info_file, 'rt', encoding="ISO-8859-1") as f:
        lines = f.readlines()

    user_info_dict = {}
    for line in lines:
        line = line.strip().split('|')
        user_id = int(line[0])
        age = int(line[1])
        gender = 'Male' if line[2] == 'M' else 'Female'
        user_info_dict[user_id] = {
            'age': age,
            'gender': gender
        }
    return user_info_dict

def load_item_info(info_file):
    with open(info_file, 'rt', encoding="ISO-8859-1") as f:
        lines = f.readlines()
    
    genre_list = ['unknown', 'Action', 'Adventure' ,'Animation', 'Children\'s', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
    item_info_dict = {}
    for line in lines:
        line = line.strip().split('|')
        item_id = int(line[0])
        title = line[1][:-7]
        if line[2] == '':
            line[2] = '01-Jan-1900'
        date = datetime.strptime(line[2], "%d-%b-%Y")
        genre_mask = [int(x) for x in line[-19:]]
        genre_idx = np.nonzero(genre_mask)[0]
        genre = ', '.join([genre_list[x] for x in genre_idx])

        item_info_dict[item_id] = {
            'title': title,
            'date': date,
            'genre': genre
        }
    return item_info_dict

def user_item_dict(df):
    # user/item_id_dict: old to new id
    unique_users = pd.unique(df['user']).tolist()
    user_id_dict = {x: i for i, x in enumerate(unique_users)}

    unique_items = pd.unique(df['item']).tolist()
    item_id_dict = {x: i for i, x in enumerate(unique_items)}
    
    return user_id_dict, item_id_dict

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', type=str, default='data/ml-100k')
    args = parser.parse_args()

    data_file = os.path.join(args.data_dir, 'u.data')
    full_data = pd.read_csv(data_file, delimiter='\t', names=['user', 'item', 'rating', 'timestamp'])
    
    user_id_map, item_id_map = user_item_dict(full_data)
    
    item_file = os.path.join(args.data_dir, 'u.item')
    item_info_dict = load_item_info(item_file)
    
    user_file = os.path.join(args.data_dir, 'u.user')
    user_info_dict = load_user_info(user_file)
    
    print('Reset existing db...')
    print(f'{User.query.delete()} users deleted...')
    print(f'{Movie.query.delete()} movies deleted...')
    print(f'{Interaction.query.delete()} iteractions deleted...')

    # Add user
    for old_u_id in user_id_map:
        user_id = user_id_map[old_u_id]
        user_info = user_info_dict[old_u_id]
        
        if User.query.filter_by(id=user_id).first():
            continue

        user = User(id=user_id, age=user_info['age'], gender=user_info['gender'])
        db.session.add(user)
    db.session.commit()

    # Add movie
    for old_i_id in item_id_map:
        item_id = item_id_map[old_i_id]
        item_info = item_info_dict[old_i_id]

        if Movie.query.filter_by(id=item_id).first():
            print(Movie.query.filter_by(id=item_id).first())
            continue

        movie = Movie(id=item_id, **item_info)
        db.session.add(movie)
    db.session.commit()

    for row in tqdm(full_data.itertuples(), total=len(full_data)):
        user = user_id_map[row.user]
        item = item_id_map[row.item]
        rating = float(row.rating)
        timestamp = int(row.rating)

        user = User.query.filter_by(id=user).first()
        item = Movie.query.filter_by(id=item).first()

        I = Interaction(user_id=user.id, movie_id=item.id, rating=rating, timestamp=timestamp)
        user.movies.append(I)
        item.users.append(I)
        db.session.add(I)
    db.session.commit()