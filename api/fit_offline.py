import os
import sys
import argparse
from pathlib import Path

WEB_DIR_PATH = Path(__file__).resolve().parents[1] / "backend"
DB_PATH = WEB_DIR_PATH / "app.db"
sys.path.append(WEB_DIR_PATH.__str__())

from config import Config, BASE_DIR
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.model import User, Movie, Interaction
import numpy as np
import scipy.sparse as sp
from tqdm import tqdm
from recommend.utils import load_rating_matrix_from_db, split_train_test
from recommend.models import model_to_cls
from recommend.evaluate import extract_top_k, evaluate

parser = argparse.ArgumentParser()
parser.add_argument('--model', type=str, default='ItemKNN')
parser.add_argument('--save_dir', type=str, default='recommend/ckpt')
parser.add_argument('--test_ratio', type=float, default=0.1)
parser.add_argument('--k', type=int, default=100)
args = parser.parse_args()

app = Flask(__name__)
app.config.from_object(Config)
app.app_context().push()

db = SQLAlchemy()
db.init_app(app)

rating_matrix = load_rating_matrix_from_db(User, Interaction)
num_users, num_items = rating_matrix.shape

train_matrix, test_matrix = split_train_test(rating_matrix, test_ratio=args.test_ratio, shape=(num_users, num_items))
model_cls = model_to_cls[args.model]
model = model_cls()

print('Train start...')
model.fit(train_matrix, save_path=args.save_dir)

print('Train finished...')

prediction = model.predict(train_matrix)
topk = extract_top_k(prediction, args.k)

# Evaluate
scores = evaluate(topk, test_matrix, args.k)

model.save(args.save_dir)