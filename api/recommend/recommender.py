import pickle
import numpy as np

from recommend.models import model_to_ckpt, model_to_cls

class RecommenderWrapper:
    def __init__(self) -> None:
        self.model_name = None
        self.model = None
    
    def set_model(self, new_model):
        if self.model == None or self.model_name != new_model:
            self.model_name = new_model
            self.model = model_to_cls[new_model]()
            self.model.restore(model_to_ckpt[new_model])
        
    def recommend(self, user_context):
        # user context to user vec
        user_item_ids = [int(i) for i in user_context]

        # recommend
        recommendation = self.model.recommend(user_item_ids)

        return recommendation
