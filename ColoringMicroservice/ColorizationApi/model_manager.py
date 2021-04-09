from ColorizationApi.singleton import Singleton
from ColorizationApi.fastai_model_20 import fastai_model_20
from ColorizationApi.fastai_model_40 import fastai_model_40
from ColorizationApi.non_fastai_model import non_fastai_model
import torch

class model_manager(metaclass=Singleton):
    def __init__(self):
        print("Initializing models")
        self.fastai_model_40 = fastai_model_40()
        self.fastai_model_20 = fastai_model_20()
        self.non_fastai_model = non_fastai_model()
    
    def get_model(self, permission_level=0):
        if permission_level == 2:
            return self.fastai_model_40
        elif permission_level == 1:
            return self.fastai_model_20
        else:
            return self.non_fastai_model
    
    # def set_model(self, permission_level=0):
    #     if permission_level == 2:
    #         self.current_model = self.fastai_model_40
    #     elif permission_level == 1:
    #         self.current_model = self.fastai_model_20
    #     else:
    #         self.current_model = self.non_fastai_model
    
