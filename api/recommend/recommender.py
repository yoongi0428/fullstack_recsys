import pickle
import numpy as np

from recommend.models import model_to_ckpt, model_to_cls

class RecommenderWrapper:
    def __init__(self) -> None:
        self.model_name = None
        self.model = None
        # self.item_dict = data['item_dict']
        # self.new_to_old_id = {self.item_dict[i]['new_id']: i for i in self.item_dict}
    
    def set_model(self, new_model):
        if self.model == None or self.model_name != new_model:
            self.model_name = new_model
            self.model = model_to_cls[new_model]()
            self.model.restore(model_to_ckpt[new_model])
        
    def recommend(self, user_context):
        # user context to user vec
        user_item_ids = [int(i) for i in user_context]
        # user_item_ids = [10, 100, 234, 253, 236, 623, 872, 321]

        # recommend
        recommendation = self.model.recommend(user_item_ids)
        # recommendation = [4, 6, 10]

        # convert prediction to result
        # recommendation_dict = {i: self.item_dict[self.new_to_old_id[i]] for i in recommendation}

        return recommendation
