import os

from recommend.models.EASE import EASE
from recommend.models.ItemKNN import ItemKNN

BASE_DIR = 'recommend/ckpt'

model_to_ckpt = {
    'EASE': os.path.join(BASE_DIR, 'EASE_100.npy'),
    'ItemKNN': os.path.join(BASE_DIR, 'ItemKNN_100.npz')
}

model_to_cls = {
    'EASE': EASE,
    'ItemKNN': ItemKNN
}