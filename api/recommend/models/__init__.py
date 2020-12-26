import os

from recommend.models.EASE import EASE
# from models.ItemKNN import ItemKNN

BASE_DIR = 'recommend/ckpt'

model_to_ckpt = {
    'EASE': os.path.join(BASE_DIR, 'EASE_100.npy')
}

model_to_cls = {
    'EASE': EASE
}